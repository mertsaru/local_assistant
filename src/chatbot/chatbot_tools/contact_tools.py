from typing import Optional
from pydantic import BaseModel
import json

from langchain_core.tools import tool
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import telegram

from src import config

CONTACT_JSON_PATH = config.CONTACT_JSON_PATH


class Contact(BaseModel):
    telegram_number: Optional[str] = None
    email: Optional[str] = None


@tool
def add_contact(name: str, Contact: Contact):
    with open(config.CONTACT_JSON_PATH, "r", encoding="utf-8") as f:
        contacts = json.load(f)

    if name in contacts:
        raise ValueError(f"Contact with name {name} already exists.")

    new_contact = {"telegram_number": Contact.telegram_number, "email": Contact.email}

    contacts[name] = new_contact

    with open(config.CONTACT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=4, ensure_ascii=False)

    return


@tool
def update_contact(name, Contact):
    with open(config.CONTACT_JSON_PATH, "r", encoding="utf-8") as f:
        contacts = json.load(f)

    if name not in contacts:
        raise ValueError(f"Contact with name {name} does not exist.")

    if Contact.telegram_number is not None:
        contacts[name]["telegram_number"] = Contact.telegram_number
    if Contact.email is not None:
        contacts[name]["email"] = Contact.email

    with open(config.CONTACT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=4, ensure_ascii=False)

    return


@tool
def delete_contact(name: str):
    with open(config.CONTACT_JSON_PATH, "r", encoding="utf-8") as f:
        contacts = json.load(f)

    if name not in contacts:
        raise ValueError(f"Contact with name {name} does not exist.")

    contacts.pop(name)

    with open(config.CONTACT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=4, ensure_ascii=False)

    return


@tool
def send_email_to_contact(contact_name: str, email_subject: str, email_body: str):
    """Send an email to a contact.

    Args:
        contact_name (str): name of the contact to send the email to.
        email_subject (str): subject of the email.
        email_body (str): body of the email.
    """

    with open(CONTACT_JSON_PATH, "r", encoding="utf-8") as f:
        contacts = json.load(f)

    if contact_name not in contacts:
        raise ValueError(f"Contact with name {contact_name} does not exist.")

    contact = contacts[contact_name]

    if not contact.get("email"):
        raise ValueError(f"Contact {contact_name} does not have an email address.")

    sender_email = config.EMAIL_ADDRESS
    sender_password = config.EMAIL_PASSWORD
    receiver_email = contact["email"]

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = email_subject

    msg.attach(MIMEText(email_body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"Email sent to {contact_name} at {receiver_email}")
    except Exception as e:
        print(f"Failed to send email to {contact_name}. Error: {e}")
        raise e


@tool
def send_telegram_message_to_contact(name: str, message: str):
    """Send a telegram message to a contact.

    Args:
        name (str): name of the contact to send the message to.
        message (str): message to send.
    """

    with open(CONTACT_JSON_PATH, "r", encoding="utf-8") as f:
        contacts = json.load(f)

    if name not in contacts:
        raise ValueError(f"Contact with name {name} does not exist.")

    contact = contacts[name]

    if not contact.get("telegram_number"):
        raise ValueError(f"Contact {name} does not have a telegram number.")


    bot = telegram.Bot(token=config.TELEGRAM_API_KEY)

    try:
        bot.send_message(chat_id=contact["telegram_number"], text=message)
        print(f"Message sent to {name} at {contact['telegram_number']}")
    except Exception as e:
        print(f"Failed to send message to {name}. Error: {e}")
        raise e
