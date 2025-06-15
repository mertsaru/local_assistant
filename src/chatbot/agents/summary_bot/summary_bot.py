from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import OllamaLLM

from src import config

SUMMARY_LLM_SYS_PROMPT_PATH = config.SUMMARY_LLM_SYS_PROMPT_PATH

with open(SUMMARY_LLM_SYS_PROMPT_PATH, "r") as f:
    summary_llm_sys_prompt = f.read()


def summarize_page(page_text: str, model: OllamaLLM, source_text) -> str:
    summary_hist = [
        SystemMessage(summary_llm_sys_prompt.format(source_text)),
        HumanMessage(page_text),
    ]
    summary = model.invoke(summary_hist)
    return summary.content
