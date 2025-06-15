r"""Decides whether the model should use RAG, web, or nothing."""

import os
from typing_extensions import Annotated, TypedDict
import json

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import OllamaLLM

from src import config

RAG_DATA_TOPICS_PATH = config.RAG_DATA_TOPICS_PATH
DECIDER_LLM_SYS_PROMPT = config.DECIDER_LLM_SYS_PROMPT

with open(DECIDER_LLM_SYS_PROMPT, "r") as f:
    decider_llm_sys_prompt = f.read()


class Decision(TypedDict):

    web_search: Annotated[bool, "need for web search"]
    RAG: Annotated[bool, "need for RAG"]


def decide_data_source(model: OllamaLLM, question: str) -> Decision:

    if os.path.exists(RAG_DATA_TOPICS_PATH):
        with open(
            RAG_DATA_TOPICS_PATH, "r"
        ) as f:  # we open data topics every time to decide since we do not want to restart the run every time when RAG has an update
            rag_data_topics = json.load(f)
    else:
        rag_data_topics = "RAG is empty"

    history = [
        SystemMessage(decider_llm_sys_prompt.format(rag_data_topics)),
        HumanMessage(question),
    ]

    decision_model = model.with_structured_output(Decision())
    decision = decision_model.invoke(history)
    return decision
