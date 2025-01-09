from llama_index.core.llms import LLM


def get_model_providers() -> list[str]:
    return []


def get_model_config(model_provider: str) -> dict:
    raise NotImplementedError(f"model provider '{model_provider}' is not implemented")


def update_model_config(model_provider: str, conf: dict):
    raise NotImplementedError(f"model provider '{model_provider}' is not implemented")


def get_models(model_provider: str, model_type: str) -> list:
    raise NotImplementedError(
        f"'{model_type}' on model provider  '{model_provider}' is not implemented"
    )


def new_model(model_provider, model_type) -> LLM:
    raise NotImplementedError(
        f"Model type '{model_type}' on model provider '{model_provider}' is not implemented"
    )
