r"""Decides whether the model should use RAG, web, or nothing."""

import os
from pydantic import BaseModel, Field
import json

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import OllamaLLM

from src import config


with open(config.DECIDER_LLM_SYS_PROMPT, "r") as f:
    decider_llm_sys_prompt = f.read()


class Decision(BaseModel):

    web_search: bool = Field(default=False, description="Whether to use web search")
    rag_search: bool = Field(default=False, description="Whether to use RAG search")

decision_model = OllamaLLM(
    model=config.PARAMETERS["agents"]["decider_llm"],
).with_structured_output(Decision)

def decide_data_source(question: str) -> Decision:

    if os.path.exists(config.RAG_DATA_TOPICS_PATH):
        with open(
            config.RAG_DATA_TOPICS_PATH, "r"
        ) as f:  # we open data topics every time to decide since we do not want to restart the run every time when RAG has an update
            rag_data_topics = json.load(f)
    else:
        rag_data_topics = "RAG is empty"

    history = [
        SystemMessage(decider_llm_sys_prompt.format(rag_data_topics)),
        HumanMessage(question),
    ]

    decision = decision_model.invoke(history)
    return decision
