from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_ollama import OllamaLLM

from .agents.decider_llm import decider_llm
from .doc_searchers.web_search import web_search
from .utils import token_counter, chatbot_tools
from src import config


history_length_threshold = 100_000

SYS_PROMPT_PATH = config.SYS_PROMPT_PATH

with open(SYS_PROMPT_PATH, "r") as f:
    sys_prompt = f.read()


tools = {
    "set_alarm": chatbot_tools.set_alarm,
    "set_reminder": chatbot_tools.set_reminder,
    "add_to_shopping_list": chatbot_tools.add_to_shopping_list,
    "delete_from_shopping_list": chatbot_tools.delete_from_shopping_list,
    "get_shopping_list": chatbot_tools.get_shopping_list,
}


class Chatbot:

    def __init__(self):
        self.history = [  # TODO create a sql base history and save every chat there, so the model can also check sql chat history like rag and web search
            SystemMessage(sys_prompt),
            HumanMessage(
                "I am providing you some documents. I want you to answer my questions according to these documents: "
            ),
            AIMessage("Thank you for the documents, please ask your question"),
        ]
        self.sum_tokens = 0  # TODO count sys_prompt, human message and ai message

    def generate_answer(self, model: OllamaLLM, question: str, logger):

        new_doc_prompt = ""
        # run decider
        decision = decider_llm.decide_data_source(model, question)

        # if decided rag search rag
        if decision.RAG is True:
            pass  # TODO add rag

        # if decided web search, search web
        if decision.web_search is True:
            web_docs = web_search.get_search_results(question, model, logger)
            new_doc_prompt += "\n\n" + web_docs

        if new_doc_prompt is not "":
            pass  # TODO check token lenght
        else:
            new_doc_prompt_token_count = 0

        # check history length, if long delete some
        if self.sum_tokens + new_doc_prompt_token_count > history_length_threshold:
            pass  # TODO find a delete method, delete first the chat history in the middle, when it is not enough than delete part of docs

        # build history if any doc is found
        if new_doc_prompt != "":
            self.history[1] += new_doc_prompt

        # add tools to the model
        model_with_tools = model.bind_tools(list(tools.values()))

        # run model
        ai_response = model_with_tools.invoke(self.history + [HumanMessage(question)])

        ## tool calls
        if len(ai_response.tool_calls) != 0:
            tool_messages = []
            for tool in ai_response.tool_calls:
                selected_tool = tools[tool["name"].lower()]
                tool_msg = selected_tool.invoke(tool)
                tool_messages.append(tool_msg)
            tool_response = model_with_tools.invoke(
                self.history + [HumanMessage(question)] + [ai_response] + tool_messages
            )
        else:
            tool_response = []

        # update history
        self.history += (
            [HumanMessage(question)] + [ai_response] + tool_messages + tool_response
        )

        return tool_response.content if tool_response != [] else ai_response.content
