# 1. Local Assistant

*This project is still under development*

This project enables user to run a local assistant with access to Google.

## 1.1. Table of Contents

- [1. Local Assistant](#1-local-assistant)
  - [1.1. Table of Contents](#11-table-of-contents)
  - [1.2. How to Run](#12-how-to-run)
    - [Create environment](#create-environment)
    - [1.2.1. Install Conda](#121-install-conda)
  - [1.3. Customizable parameters](#13-customizable-parameters)
    - [1.3.1. Search parameters](#131-search-parameters)

## 1.2. How to Run

First you need to create an environment for the project. I used Conda environment.

### Create environment

change the name of .env.example file to .env and adjust the variables according to your case.

### 1.2.1. Install Conda

To install conda check the following link provided by Conda:

## 1.3. Customizable parameters

You can change some parameters of the project in [./src/parameters.yaml](./src/parameters.yaml)

### 1.3.1. Search parameters

number_of_pages (int): if the chatbot using web to find some answers, this parameter controls how many pages the AI should check. I do not recommend to increase the number drastically since every website check adds 2 second delay, because we do not want to warn google that we are spamming google search.
