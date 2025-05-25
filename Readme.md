# 1. Local Assistant

*This project is still under development*

This project enables user to run a local assistant with access to Google. We use only one model with different system prompts to do various tasks (such as answering questions, web search summarization, context generation of the question etc.) so we do not need big GPUs to run one model for each task.

## 1.1. Table of Contents

- [1. Local Assistant](#1-local-assistant)
  - [1.1. Table of Contents](#11-table-of-contents)
  - [1.2. Requirements](#12-requirements)
    - [Ollama](#ollama)
    - [1.2.1. Install Conda](#121-install-conda)
  - [1.3. Customizable parameters](#13-customizable-parameters)
    - [1.3.1. Search parameters](#131-search-parameters)
    - [Question Generator parameters](#question-generator-parameters)

## 1.2. Requirements

### Ollama

This project requires Ollama. You need to install Ollama for your system on the following link [Ollama github page](https://github.com/ollama/ollama).

### 1.2.1. Install Conda

we need to create an environment for the project. For that purpose, we use Conda environment.

To install conda check the following link provided by Conda:

## 1.3. Customizable parameters

You can change some parameters of the project in [./src/parameters.yaml](./src/parameters.yaml)

### 1.3.1. Search parameters

number_of_pages (int): if the chatbot using web to find some answers, this parameter controls how many pages the AI should check. I do not recommend to increase the number drastically since every website check adds 2 second delay, because we do not want to warn google that we are spamming google search.

### Question Generator parameters

number_of_gen_questions (int): To get the context of the question (or prompt) the model generates similar questions given to the original. This method increases model to find similar results to the given question.
