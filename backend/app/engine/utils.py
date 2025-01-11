from app.engine import config, models


def print_info(data_name: str):
    print("-" * 80)
    print("model_provider:", config.model_provider)
    print("data_name:", data_name)
    print("embed_model:", models.get_embed_model_name())
    print("chat_model:", models.get_chat_model_name())
    print("-" * 80)
