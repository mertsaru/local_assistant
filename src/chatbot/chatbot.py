from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_ollama import OllamaLLM

from .chatbot_tools import reminder_tools
from .agents.decider_llm import decider_llm
from . import doc_searchers
from src import config




with open(config.SYS_PROMPT_PATH, "r") as f:
    sys_prompt = f.read()


tools = { # TODO make it dynamic?
    "set_alarm": reminder_tools.set_alarm,
    "set_reminder": reminder_tools.set_reminder,
    "add_to_calendar": reminder_tools.add_to_calendar,
}

answer_gen_llm = OllamaLLM(
    model=config.PARAMETERS["agents"]["answer_gen_llm"],
).bind_tools(list(tools.values()))

class Chatbot:

    def __init__(self):
        self.history = [
            SystemMessage(sys_prompt),
            HumanMessage(
                "I am providing you some documents. I want you to answer my questions according to these documents: "
            ),
            AIMessage("Thank you for the documents, please ask your question"),
        ]

        self.outer_text_sources = []  # this is used to store the text sources of the documents, so the model can use them in the answer generation

        self.used_ids = []


    async def generate_answer(self, question: str):

        new_doc_prompt = ""
        # run decider
        decision = decider_llm.decide_data_source(question)

        # if decided rag search rag
        if decision.rag_search is True:
            rag_docs = doc_searchers.rag_search.get_rag_docs(question=question, used_ids=self.used_ids)
            new_doc_prompt += rag_docs

        # if decided web search, search web
        if decision.web_search is True:
            web_docs = await doc_searchers.web_search.get_search_results(question)
            new_doc_prompt += "\n\n" + web_docs

        if new_doc_prompt is not "":
            new_doc_prompt_token_count = answer_gen_llm.get_num_tokens(new_doc_prompt)
        else:
            new_doc_prompt_token_count = 0

        # check history length, if long delete some
        if  + new_doc_prompt_token_count > history_length_threshold:
            pass  # TODO delete earliest history from used_ids and outer_text_sources

        # build history if any doc is found
        if new_doc_prompt != "":
            self.history[1] += new_doc_prompt



        # run model
        ai_response = answer_gen_llm.invoke(self.history + [HumanMessage(question)])

        ## tool calls
        if len(ai_response.tool_calls) != 0:
            tool_messages = []
            for tool in ai_response.tool_calls:
                selected_tool = tools[tool["name"].lower()]
                tool_msg = selected_tool.invoke(tool)
                tool_messages.append(tool_msg)
            tool_response = answer_gen_llm.invoke(
                self.history + [HumanMessage(question)] + [ai_response] + tool_messages
            )
        else:
            tool_response = []

        # update history
        self.history += (
            [HumanMessage(question)] + [ai_response] + tool_messages + tool_response
        )

        return tool_response.content if tool_response != [] else ai_response.content
