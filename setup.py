import nltk
from huggingface_hub import snapshot_download
import json

from src import config


# cross encoder model
snapshot_download(
    repo_id="intfloat/multilingual-e5-base",
    local_dir=config.CROSS_ENCODER_PATH,
    local_dir_use_symlinks=False,
)


# sentence splitter
nltk.download("punkt_tab")


# create folders/files

## metadata

### contact.json
with open(config.CONTACT_JSON_PATH, "w") as f:
    json.dump(
        {},f)
### shopping_list.json
with open(config.SHOPPING_LIST_PATH, "w") as f:
    json.dump(
        {},f)