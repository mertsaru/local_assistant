import numpy as np
from torch import Tensor
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel

from src import config


model = AutoModel.from_pretrained(config.CROSS_ENCODER_PATH)
tokenizer = AutoTokenizer.from_pretrained(config.CROSS_ENCODER_PATH)


def _average_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


def _compare(input_texts: list[str]) -> list:
    batch_dict = tokenizer(
        input_texts, max_length=512, padding=True, truncation=True, return_tensors="pt"
    )

    outputs = model(**batch_dict)
    embeddings = _average_pool(outputs.last_hidden_state, batch_dict["attention_mask"])

    # normalize embeddings
    embeddings = F.normalize(embeddings, p=2, dim=1)
    scores = (embeddings[:1] @ embeddings[1:].T) * 100
    scores = scores.detach().squeeze(0)
    scores = scores.numpy()
    return scores


def find_best_indices(original_prompt, compared_texts: list, best_n_pages:int, threshold) -> list[int]:
    # Tokenize the input texts
    input_texts = [f"query: {original_prompt}"] + [
        f"passage: {text}" for text in compared_texts
    ]

    scores = _compare(input_texts)

    best_n_texts = min(best_n_pages, len(compared_texts))

    best_n_arg_scores = np.argsort(scores)[::-1][:best_n_texts]
    best_n_arg_scores = best_n_arg_scores.tolist()

    if threshold != 0:
        return [
            i
            for i in best_n_arg_scores
            if scores[i] >= threshold * 100
        ]
    else:
        return best_n_arg_scores if isinstance(best_n_arg_scores, list) else [best_n_arg_scores]
