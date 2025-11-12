import json


from langchain_core.tools import tool

from src.config import SHOPPING_LIST_PATH


# TODO make shopping list categorized by aisle


@tool
def add_to_shopping_list(items: list[str]) -> None:
    """Add items to the shopping list.

    Args:
        items (list[str]): The items to add to the shopping list.
    """
    with open(SHOPPING_LIST_PATH, "r", encoding="utf-8") as f:
        shopping_list: list[str] = json.load(f)

    shopping_list.extend(items)

    with open(SHOPPING_LIST_PATH, "w", encoding="utf-8") as f:
        json.dump(shopping_list, f, ensure_ascii=False, indent=4)
    
    return f"Added {items} to the shopping list."


@tool
def delete_from_shopping_list(items: list[str]) -> None:
    """Delete items from the shopping list.

    Args:
        items (list[str]): The items to delete from the shopping list.
    """
    with open(SHOPPING_LIST_PATH, "r", encoding="utf-8") as f:
        shopping_list: list[str] = json.load(f)

    for item in items:
        if item in shopping_list:
            shopping_list.remove(item)

    with open(SHOPPING_LIST_PATH, "w", encoding="utf-8") as f:
        json.dump(shopping_list, f, ensure_ascii=False, indent=4)


@tool
def get_shopping_list() -> list[str]:
    """Get the current shopping list.

    Returns:
        list[str]: The current shopping list.
    """
    with open(SHOPPING_LIST_PATH, "r", encoding="utf-8") as f:
        shopping_list: list[str] = json.load(f)
    return shopping_list
