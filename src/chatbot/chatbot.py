from copy import deepcopy
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain.chat_models import init_chat_model
from langchain_core.messages.utils import count_tokens_approximately

from .chatbot_tools import reminder_tools
from .agents.decider_llm import decider_llm
from . import doc_searchers
from src import config


with open(config.SYS_PROMPT_PATH, "r") as f:
    sys_prompt = f.read()


tools = {  # TODO make it dynamic?
    "set_alarm": reminder_tools.set_alarm,
}

answer_gen_llm = init_chat_model(
    model=config.PARAMETERS["agents"]["answer_gen_llm"],model_provider="ollama",
).bind_tools(list(tools.values()))


class Chatbot:

    def __init__(self):
        self._history = [  # TODO store history in postgres
            SystemMessage(sys_prompt),
            HumanMessage(
                "I am providing you some documents. I want you to answer my questions according to these documents: "
            ),
            AIMessage("Thank you for the documents, please ask your question"),
        ]

        self._outer_text_sources = (
            []
        )  # store the text sources of the documents, so the model can use them in the answer generation

        self._used_ids = []

        self._last_token_count = 0

    async def generate_answer(self, question: str):

        new_doc_prompt = ""
        # run decider
        decision = decider_llm.decide_data_source(question)

        # if decided rag search rag # TODO use threads to run search processes at the same time
        if decision.rag_search is True:
            doc_packages, doc_ids = doc_searchers.rag_search.get_rag_docs(
                question=question, used_ids=self._used_ids
            )

            self._used_ids += doc_ids
            self._outer_text_sources += doc_packages

        # if decided web search, search web
        if (
            decision.web_search is True
        ):  # Web search is one time only, it means it does not stay in the memory, since web search can be big than rag search
            web_docs = await doc_searchers.web_search.get_search_results(question)
            new_doc_prompt += "\n\n" + web_docs

        if new_doc_prompt != "":
            new_doc_prompt_token_count = count_tokens_approximately([new_doc_prompt])
        else:
            new_doc_prompt_token_count = 0

        # check history length, if long delete some
        if (
            self._last_token_count
            + new_doc_prompt_token_count
            + count_tokens_approximately(self._outer_text_sources)
            > config.PARAMETERS["chat_history"]["history_length_threshold"]
        ):
            extra_tokens = (
                self._last_token_count
                + new_doc_prompt_token_count
                - config.PARAMETERS["chat_history"]["history_length_threshold"]
            )

            self._truncate_chat(extra_tokens)
        new_doc_prompt += "".join(
            [f"\n\n{text}" for text in self._outer_text_sources])

        history_copy = deepcopy(self._history)

        # build history if any doc is found
        if new_doc_prompt != "":
            history_copy[1].content += new_doc_prompt

        # run model
        ai_response = answer_gen_llm.invoke(history_copy + [HumanMessage(question)])
        
        ## tool calls
        tool_messages = []
        if len(ai_response.tool_calls) != 0:
            for tool in ai_response.tool_calls:
                selected_tool = tools[tool["name"].lower()]
                tool_msg = selected_tool.invoke(tool)
                tool_messages.append(tool_msg)
            tool_response = answer_gen_llm.invoke(
                history_copy + [HumanMessage(question)] + [ai_response] + tool_messages
            )
            input_tokens = tool_response.usage_metadata["input_tokens"]

        else:
            input_tokens = ai_response.usage_metadata["input_tokens"]
            tool_response = []

        # update history
        self._history += (
            [HumanMessage(question)] + [ai_response] + tool_messages + tool_response
        )

        self._last_token_count = input_tokens

        return tool_response.content if tool_response != [] else ai_response.content

    def _truncate_chat(self, extra_tokens):
        num_tokens = 0
        rag_token_count = count_tokens_approximately(self._outer_text_sources)
        if rag_token_count <= extra_tokens:
            for i, text in enumerate(self._outer_text_sources):
                num_tokens += count_tokens_approximately([text])
                if num_tokens > extra_tokens:
                    self._outer_text_sources = self._outer_text_sources[i + 1 :]
                    self._used_ids = self._used_ids[i + 1 :]
                    break
        else:  # if rag docs is not enough to cover the extra tokens, remove all rag docs and then start removing chat history
            self._outer_text_sources = []
            self._used_ids = []
            num_tokens = rag_token_count
            for i, message in enumerate(
                self._history[3:]
            ):  # skip system and initial messages
                if isinstance(message, HumanMessage) and num_tokens >= extra_tokens:
                    self._history = self._history[:3] + self._history[i + 3 :]
                    break

                num_tokens += count_tokens_approximately([message.content])
