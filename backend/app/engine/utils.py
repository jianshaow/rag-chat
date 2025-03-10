import logging
from app.engine import models, setting

logger = logging.getLogger(__name__)

MODEL_INFO_LOG_TEMPLATE = """
%s
moel_provider: %s
data_name: %s
embed_model: %s
chat_model: %s
%s
"""


def log_model_info(data_dir: str):
    logger.info(
        MODEL_INFO_LOG_TEMPLATE,
        "-" * 80,
        setting.get_model_provider(),
        data_dir,
        models.get_embed_model_name(),
        models.get_chat_model_name(),
        "-" * 80,
    )
