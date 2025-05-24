import os

import requests
from googlesearch import search
import yaml
from bs4 import BeautifulSoup
from langchain_ollama import OllamaLLM

PARAM_PATH = os.getenv("PARAM_PATH")
with open(PARAM_PATH,"r") as f:
    parameters = yaml.safe_load(f)

number_of_pages = parameters["search"]["number_of_pages"]


class SearchLLM():

    def __init__(self, llm_model):
        model = llm_model

    @classmethod
    def _find_pages(cls,question, number_of_pages=number_of_pages):
        website_lists = search(question, stop=number_of_pages, pause=2)
        return website_lists

    @classmethod
    def _read_page(cls,url):
        page = requests.get(url).content
        soup = BeautifulSoup(page, 'html.parser')
        return soup


    @classmethod
    def _summarize_page(cls,page_text:str):
        pass

    def search_results(self):
        pass