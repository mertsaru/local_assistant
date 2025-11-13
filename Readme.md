# 1. Local Assistant

This project enables user to run a local assistant with access to Google Search, Gmail, Whatsapp, and Telegram (Gmail Whatsapp and Telegram is still on the  process). We use only one model with different system prompts to do various tasks (such as answering questions, web search summarization, context generation of the question etc.) so we do not need big GPUs to run one model for each task. However, because we are only using one model to do couple of tasks to save GPU power, we are sacrificing from processing time. Besides, the model has only one chat memory (one chat instance) and hence for only one user, (however one can upgrade it by logging the conversations into a SQL database.) That is why this is just a fun project for me and it should not be an end product because of the latency, and privacy issues. I would like to run the code in my home server, so I would have a personal AI assistant.

## 1.1. Table of Contents

- [1. Local Assistant](#1-local-assistant)
  - [1.1. Table of Contents](#11-table-of-contents)
  - [1.2. Requirements](#12-requirements)
    - [1.2.1. Ollama](#121-ollama)
    - [CUDA](#cuda)
    - [Tesseract (Optional)](#tesseract-optional)
    - [1.2.2. Python Setup](#122-python-setup)
    - [1.2.3. Virtual Environment](#123-virtual-environment)
    - [1.2.4. Running Setup.py](#124-running-setuppy)
  - [1.3.1 Dotenv and Parameters](#131-dotenv-and-parameters)
  - [RAG Installation](#rag-installation)
    - [Text files](#text-files)
      - [PDF files](#pdf-files)
    - [Images with text](#images-with-text)
- [How To Run](#how-to-run)

## 1.2. Requirements

### 1.2.1. Ollama

This project requires Ollama. You need to install Ollama for your system on the following link [Ollama github page](https://github.com/ollama/ollama). After that you can install the model you want to use for the project by using the following command on the cmd:

`ollama pull <model-name:version>`

### CUDA

Project uses CUDA to interpret images, however CUDA is not necessary for the process, one can use CPU without any installation or change. The project uses CUDA 12.8 if CUDA is available. You can still use older CUDA versions, if you configure the pytorch setup. However the default CUDA version for this project is 12.8.

### Tesseract (Optional)

Tesseract is used to extract text from images. If you want to use the RAG that extracts text from images, then install Tesseract. You can install it on:

[Tesseract install](https://github.com/UB-Mannheim/tesseract?tab=readme-ov-file#installing-tesseract)

While installing Tesseract on your system, I highly suggest adding optional languages during the installation if you planning to use non-english, or mathematical text.

### 1.2.2. Python Setup

The project uses [uv-astral](https://docs.astral.sh/uv/) as the environment manager. You can install it with various methods. To install check the [astal install website](https://docs.astral.sh/uv/#installation)

### 1.2.3. Virtual Environment

On the project directory run `uv sync` to setup the Environment

### 1.2.4. Running Setup.py

Downloads the other necessary AI models to run the RAG database, and setup the history database. To use it be sure  your environment is active and run `python -m setup` or run the python script through uv by `uv run python -m setup`

## 1.3.1 Dotenv and Parameters

Copy or change the .env.example file to .env file and fill (or change) the parameters.

- EMAIL_ADDRESS: your email address to send the emails (gmail)
- EMAIL_PASSWORD: Duhh
- TELEGRAM_API_KEY: You can find it through telegram app.

- NUMBER_OF_PAGES: num of pages to search when using web search
- NUMBER_OF_GEN_QUESTIONS: we generate question to find better matches.
- BEST_N_PAGES: number of pages to feed the AI

- NUMBER_OF_RETRIEVALS: number of documents that rag finds with each generated question

- THRESHOLD: Similarity likelyhood of the found pages to the original question
- BEST_N_PAGES: best pages to feed the chatbot through the rag process

These are llm models, one can use the same model or change the models to improve performance or speed (not at the same time most of the time) of one AI process. There is no multi-threading yet so it will not increase the speed drastically

- DECIDER_LLM: chooses whether to use rag or web search
- QUESTION_GEN_LLM: generates similar question to original prompt to increase the context awareness
- SUMMARY_LLM: summarizes pages and documents to save token count
- ANSWER_GEN_LLM: end point of the model, which generates answer or chooses tools
- TOPIC_FINDER_LLM: while installing files to RAG, topic finder names the topics and saves in json, so the model would know what it can get from RAG.

- HISTORY_LENGTH_THRESHOLD: After the threshold of tokens we start to delete the documents or chat history to disallow chat-length to go high

The API runs on uvicorn, if one want they can also run with gunicorn but one need to use cmd for that. But uvicorn parameters are below.

- PORT: default to 10102
- HOST:default to 0.0.0.0
- WORKERS: default to 1


## RAG Installation

(in progress)

### Text files

(in progress)

#### PDF files

(in progress)

### Images with text

if you want to add more language support, you need to first add the language to Tesseract during the installation. If you haven't, install Tesseract again with the required language. Then create the language folder in [data/img_to_text_files](./data/img_to_text_files). The language folder name should be same with the language input with the [pytesseract](https://github.com/madmaze/pytesseract) module.

# How To Run

To run the project with uvicorn while in the python environment use

```cmd
python -m src.main
```

If you want to run on development mode and want to see the text on cmd use

```cmd
python -m src.main --dev
```


If you want to use gunicorn than first you need to install gunicorn. Then run

```cmd
gunicorn -w <Worker_num> -k uvicorn.workers.UvicornWorker src.main:app -b <HOST>:<PORT>
```
