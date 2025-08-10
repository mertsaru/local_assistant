from typing import Annotated, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import OllamaLLM

from src import config


class Topic(TypedDict):
    topic: Annotated[str, "Topic of the text"]

with open(config.TOPIC_FINDER_LLM_SYS_PROMPT_PATH, "r") as f:
    topic_finder_llm_sys_prompt = f.read()

topic_finder_llm = OllamaLLM(
    model=config.PARAMETERS["agents"]["topic_finder_llm"],
).with_structured_output(Topic())


def get_topic(text:str, current_topics:list) -> str:
    topic_hist = [
        SystemMessage(topic_finder_llm_sys_prompt.format(current_topics)),
        HumanMessage(text),
    ]
    text_topic = topic_finder_llm.invoke(topic_hist)
    return text_topic["topic"]
