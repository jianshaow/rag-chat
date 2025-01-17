import logging
from app.engine import config, models

logger = logging.getLogger(__name__)

MODEL_INFO_LOG_TEMPLATE = "model info:\n%s\nmoel_provider: %s\ndata_name: %s\nembed_model: %s\nchat_model: %s\n%s"


def log_model_info(data_name: str):
    logger.info(
        MODEL_INFO_LOG_TEMPLATE,
        "-" * 80,
        config.model_provider,
        data_name,
        models.get_embed_model_name(),
        models.get_chat_model_name(),
        "-" * 80,
    )
