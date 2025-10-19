# TODO fill the setup

import nltk
from huggingface_hub import snapshot_download

from src import config


# install models


## embedding encoder


## cross encoder model


snapshot_download(
    repo_id="intfloat/multilingual-e5-base",
    local_dir=config.CROSS_ENCODER_PATH,
    local_dir_use_symlinks=False,
)


## interpreter

## sentence splitter
nltk.download("punkt_tab")


# create folders/files

## metadata

### contact.json

### shopping_list.json
