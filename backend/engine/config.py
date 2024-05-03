import os
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingModelType
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.llms.gemini import Gemini

data_base_dir = os.environ.get("DATA_BASE_DIR", "data")
chroma_base_dir = os.environ.get("CHROMA_BASE_DIR", "chroma")
model_spec = os.environ.get("MODEL_SPEC", "openai")

default_question = "What did the author do growing up?"


__model_spec = {
    "openai": {
        "en_embed_model": os.environ.get(
            "EN_EMBED_MODEL", OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002
        ),
        "zh_embed_model": os.environ.get(
            "ZH_EMBED_MODEL", OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002
        ),
        "default_embed_model": OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002,
        "embed_model_class": OpenAIEmbedding,
        "llm_model_class": OpenAI,
    },
    "gemini": {
        "embed_model_class": GeminiEmbedding,
        "llm_model_class": Gemini,
    },
}


def get_db_path():
    return os.path.join(chroma_base_dir, model_spec)


def get_model_config():
    return __model_spec[model_spec]


def embed_model(data_name: str):
    model_config = get_model_config()
    model_class = model_config["embed_model_class"]

    if model_class == OpenAIEmbedding:
        if data_name.startswith("en"):
            model = model_config["en_embed_model"]
        elif data_name.startswith("zh"):
            model = model_config["zh_embed_model"]
        else:
            model = model_config["default_embed_model"]
        return model_class(model=model)

    return model_class()


def chat_model():
    model_config = get_model_config()
    model_class = model_config["llm_model_class"]
    return model_class()


def get_config():
    return {
        "data_base_dir": data_base_dir,
        "chroma_base_dir": chroma_base_dir,
        "model_spec": model_spec,
    }


def update_config(conf: dict):
    global data_base_dir, chroma_base_dir, model_spec
    data_base_dir = conf.get("data_base_dir", data_base_dir)
    chroma_base_dir = conf.get("chroma_db_dir", chroma_base_dir)
    model_spec = conf.get("model_spec", model_spec)


if __name__ == "__main__":
    print(get_config())
