from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import OllamaLLM

from src import config


with open(config.SUMMARY_LLM_SYS_PROMPT_PATH, "r") as f:
    summary_llm_sys_prompt = f.read()

summary_llm = OllamaLLM(
    model=config.PARAMETERS["agents"]["summary_llm"],
)


def summarize_page(page_text: str, source_text) -> str:
    summary_hist = [
        SystemMessage(summary_llm_sys_prompt.format(source_text)),
        HumanMessage(page_text),
    ]
    summary = summary_llm.invoke(summary_hist)
    return summary.content
