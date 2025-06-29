# 1. Local Assistant

*This project is still under development*

This project enables user to run a local assistant with access to Google Search, Gmail, Whatsapp, and Telegram. We use only one model with different system prompts to do various tasks (such as answering questions, web search summarization, context generation of the question etc.) so we do not need big GPUs to run one model for each task. However, because we are only using one model to do couple of tasks to save GPU, we are sacrificing from processing time. That is why this is just a fun project for me and it should not be an end product because of the latency issues. I would like to run the code in my home server, so I would have a personal AI voice assistant.

**!BEWARE!: There is no voice recognition system, so your spouse or your kids can also send messages using the voice talk function.**

## 1.1. Table of Contents

- [1. Local Assistant](#1-local-assistant)
  - [1.1. Table of Contents](#11-table-of-contents)
  - [1.2. Requirements](#12-requirements)
    - [1.2.1. Ollama](#121-ollama)
    - [1.2.2. Python Setup](#122-python-setup)
    - [1.2.3. VirtualEnvironment](#123-virtualenvironment)
    - [1.2.4. Running Setup.py](#124-running-setuppy)
  - [1.3. Customizable parameters](#13-customizable-parameters)
    - [1.3.1. Search parameters](#131-search-parameters)
    - [1.3.2. Question Generator parameters](#132-question-generator-parameters)
  - [RAG Installation](#rag-installation)
    - [Text files](#text-files)
      - [PDF files](#pdf-files)
    - [Images with text](#images-with-text)
    - [Images without text](#images-without-text)

## 1.2. Requirements

### 1.2.1. Ollama

This project requires Ollama. You need to install Ollama for your system on the following link [Ollama github page](https://github.com/ollama/ollama).

### 1.2.2. Python Setup

### 1.2.3. VirtualEnvironment

### 1.2.4. Running Setup.py

Downloads the other necessary AI models to run the RAG database, and setup the history database.

## 1.3. Customizable parameters

You can change some parameters of the project in [./src/parameters.yaml](./src/parameters.yaml)

### 1.3.1. Search parameters

number_of_pages (int): if the chatbot using web to find some answers, this parameter controls how many pages the AI should check. I do not recommend to increase the number drastically since every website check adds 2 second delay, because we do not want to warn google that we are spamming google search.

### 1.3.2. Question Generator parameters

number_of_gen_questions (int): To get the context of the question (or prompt) the model generates similar questions given to the original. This method increases model to find similar results to the given question.

## RAG Installation

### Text files

#### PDF files

### Images with text

### Images without text
