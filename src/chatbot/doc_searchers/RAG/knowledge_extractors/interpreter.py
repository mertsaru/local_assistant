# Load model directly

import torch
import requests
from PIL import Image
from transformers import AutoProcessor, AutoModelForImageTextToText

from src import config

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
processor = AutoProcessor.from_pretrained(config.INTERPRETER_MODEL_PATH)
model = AutoModelForImageTextToText.from_pretrained(config.INTERPRETER_MODEL_PATH).to(
    device
)


def interpret(path: str):

    with Image.open(path) as img:
        img = img.convert("RGB")

    inputs = processor(img, return_tensors="pt").to(device)

    out = model.generate(**inputs)
    interpretation = processor.decode(out[0], skip_special_tokens=True)

    return interpretation
