# 1. Local Assistant

*This project is still under development*

This project enables user to run a local assistant with access to Google Search, Gmail, Whatsapp, and Telegram. We use only one model with different system prompts to do various tasks (such as answering questions, web search summarization, context generation of the question etc.) so we do not need big GPUs to run one model for each task. However, because we are only using one model to do couple of tasks to save GPU power, we are sacrificing from processing time. Besides, the model has a chat short memory (one chat instance) and hence for only one user, (however one can upgrade it by logging the conversations into a RAG database.) That is why this is just a fun project for me and it should not be an end product because of the latency, and privacy issues. I would like to run the code in my home server, so I would have a personal AI voice assistant.

**!BEWARE!: There is no voice recognition system, so your spouse or your kids can also send messages using the voice talk function.**

## 1.1. Table of Contents

- [1. Local Assistant](#1-local-assistant)
  - [1.1. Table of Contents](#11-table-of-contents)
  - [1.2. Requirements](#12-requirements)
    - [1.2.1. Ollama](#121-ollama)
    - [CUDA](#cuda)
    - [Tesseract (Optional)](#tesseract-optional)
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

### CUDA

Project uses CUDA to interpret images, however CUDA is not necessary for the process, one can use CPU without any installation or change. The project uses CUDA 12.8 if CUDA is available. You can still use older CUDA versions, if you configure the pytorch setup. However the default CUDA version for this project is 12.8.

### Tesseract (Optional)

Tesseract is used to extract text from images. If you want to use the RAG that extracts text from images, then install Tesseract. You can install it on:

[apt-get install tesseract-ocr libtesseract-dev libleptonica-dev pkg-config](https://github.com/UB-Mannheim/tesseract?tab=readme-ov-file#installing-tesseract)

While installing Tesseract on your system, I highly suggest adding optional languages during the installation if you planning to use non-english, or mathematical text.

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

if you want to add more language support, you need to first add the language to Tesseract during the installation. If you haven't, install Tesseract again with the required language. Then create the language folder in [data/img_to_text_files](./data/img_to_text_files). The language folder name should be same with the language input with the [pytesseract](https://github.com/madmaze/pytesseract) module.

### Images without text
