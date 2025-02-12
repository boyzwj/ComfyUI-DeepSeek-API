from .api_config import DeepSeekAPIConfig
from .api_chat import DeepSeekChat


NODE_CLASS_MAPPINGS = {
    "DeepSeekAPIConfig": DeepSeekAPIConfig,
    "DeepSeekChat": DeepSeekChat,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DeepSeekAPIConfig": "LLM API Model Selector",
    "DeepSeekChat": "LLM Model Input Box",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
