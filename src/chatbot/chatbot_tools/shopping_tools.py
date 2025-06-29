from langchain_core.tools import tool


@tool
def add_to_shopping_list(items: list[str]):
    pass


@tool
def delete_from_shopping_list(items: list[str]):
    pass


@tool
def get_shopping_list():
    pass
