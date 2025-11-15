import logging
from app.engine import models, setting

logger = logging.getLogger(__name__)

MODEL_INFO_LOG_TEMPLATE = """
%s
moel_provider: %s
embed_model: %s
chat_model: %s
%s
"""

TOOL_INFO_LOG_TEMPLATE = """
%s
tool_name: %s
tool_config: %s
%s
"""


def log_model_info():
    logger.info(
        MODEL_INFO_LOG_TEMPLATE,
        "-" * 80,
        setting.get_model_provider(),
        models.get_embed_model_name(),
        models.get_chat_model_name(),
        "-" * 80,
    )


def log_tool_info(data_dir: str):
    tool_set = setting.get_tool_set()
    if tool_set == "retriever":
        tool_config = f"data_dir={data_dir}"
    else:
        tool_config = f"mcp_server={setting.get_mcp_server()}"
    logger.info(
        TOOL_INFO_LOG_TEMPLATE,
        "-" * 80,
        setting.get_tool_set(),
        tool_config,
        "-" * 80,
    )
