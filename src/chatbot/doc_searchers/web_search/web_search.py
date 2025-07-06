from typing import Generator, Any, Optional 
from pydantic import BaseModel
from logging import Logger
from operator import itemgetter


from httpx import HTTPError
import requests
from googlesearch import search
import yaml
from bs4 import BeautifulSoup
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import OllamaLLM


from src import config
from src.chatbot import agents


# objects
class Page(BaseModel):
    url: str
    page_title: str
    page_text: str


# parameters
number_of_pages = config.PARAMETERS["search"]["number_of_pages"]


def _find_pages(
    question, number_of_pages=number_of_pages
) -> Generator[str | Any, Any, None]:
    website_lists = search(question, stop=number_of_pages, pause=2)
    return website_lists


def _read_page(url: str, logger: Logger) -> Optional[BeautifulSoup]:
    try:
        page = requests.get(url).content
        soup = BeautifulSoup(page, "html.parser")
        return soup
    except HTTPError as e:
        logger.warning(e)
        return


def get_search_results(question: str, model, logger):
    url_set = set()

    # context awareness
    generated_questions = agents.question_generator.generate_questions(
        model,
        question,
        number_of_gen_questions=config.PARAMETERS["question_generator"][
            "number_of_gen_questions"
        ],
    )

    # find pages
    for question in generated_questions:
        page_urls = _find_pages(question)
        url_set.update(page_urls)

    # summarize pages
    page_summary_list = list()
    for url in url_set:
        page_data = _read_page(url, logger)
        if page_data is not None:
            page_title = page_data.title.name
            page_text = page_data.get_text()
            page_summary = agents.summary_bot.summarize_page(page_text, model, question)
            page_summary_list.append(Page(url, page_title, page_summary))

    # select best pages related to the question
    best_page_summary_indices = agents.cross_encoder.find_best_indices(
        [page.page_text for page in page_summary_list],
        best_n_pages=config.PARAMETERS["question_generator"]["best_n_pages"],
    )
    getter = itemgetter(*best_page_summary_indices)
    best_page_summaries = getter(page_summary_list)

    search_result_package = "\n".join(
        f"""URL: {page.url}
        Title: {page.page_title}
        content: {page.page_text}
        """
        for page in best_page_summaries
    )
    return search_result_package
