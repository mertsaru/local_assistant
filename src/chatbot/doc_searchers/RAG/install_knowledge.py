r"""installs files in data to RAG. If the file is already installed to RAG, then the system finds it has already been installed by the hashing of the text and does not import again.

The data searched in Llama-index DB since Llama-index DB built with smaller chunk texts, then the source document retrieved from data folder. Then the model summarizes the document to feed to the model.
"""
