from transformers import AutoTokenizer, AutoModel
import torch

from src import config

CROSS_ENCODER_PATH = config.CROSS_ENCODER_PATH

# Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def cross_check(cross_encoder_model, cross_encoder_tokenizer, source_sentence: str, target_sentence: str):

    # Tokenize sentences
    encoded_input = cross_encoder_tokenizer([source_sentence,target_sentence], padding=True, truncation=True, return_tensors='pt')

# Compute token embeddings
    with torch.no_grad():
        model_output = cross_encoder_model(**encoded_input)

    # Perform pooling. In this case, max pooling.
    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
