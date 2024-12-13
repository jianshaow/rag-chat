from llama_index.core.llms import LLM

def get_api_specs() -> list[str]:
    return []


def get_api_config(api_spec: str) -> dict:
    raise NotImplementedError(f"API spec '{api_spec}' is not implemented")


def update_api_config(api_spec: str, conf: dict):
    raise NotImplementedError(f"API spec '{api_spec}' is not implemented")


def get_models(api_spec: str) -> list:
    raise NotImplementedError(f"API spec '{api_spec}' is not implemented")


def new_model(api_spec, model_type) ->LLM:
    raise NotImplementedError(
        f"Model type '{model_type}' on API spec '{api_spec}' is not implemented"
    )
