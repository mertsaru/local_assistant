from typing import Optional, BaseModel

from langchain_core.tools import tool

from src import config

CONTACT_JSON_PATH = config.CONTACT_JSON_PATH


class Contact(BaseModel):
    whatsapp_number: Optional[str] = None
    telegram_number: Optional[str] = None
    email: Optional[str] = None

@tool
def add_contact(name, Contact):
    pass


@tool
def update_contact(name, Contact):
    pass


@tool
def delete_contact(name: str):
    pass


@tool
def send_email_to_contact(name: str, subject: str, body: str):
    pass


@tool
def send_whatsapp_message_to_contact(name: str, message: str):
    pass


@tool
def send_telegram_message_to_contact(name: str, message: str):
    pass
