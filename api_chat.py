import json
import os
from openai import OpenAI
from typing import Dict, List

class DeepSeekChat:
    """
    API 对话处理器（支持JSON历史记录）
    """
    def __init__(self):
        self.history = {}

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_config": ("DICT",),
                "user_prompt": ("STRING", {
                    "default": "作为一个AI提示词专家，请你仿照范例，根据我给出的主题，生成一条符合下列要求的提示词，来让CLIP模型可以更好地理解画面主体。\n 要求共五条，请严格遵守：\n 1： 用自然语言简单句来描述画面，请避免出现过于长的，或者格式过于复杂的句子，句子中不要出现*等特殊符号。\n 2.用英语表达。 \n 3.直接给出prompt内容即可，不需要解释和说明。\n 4. 每条prompt至少50词，不超过200词。\n 5.避免模棱两可的说法。\n 例如：A 20-year-old girl with long, sleek black hair, created in a detailed 3D model. Her face is serene, with a hint of curiosity in her eyes. The rendering captures the softness of her hair and the smoothness of her complexion. The lighting is soft and diffused, creating a warm and inviting atmosphere.",
                    "multiline": True
                }),
                "system_prompt": ("STRING", {
                    "default": "20岁的女孩，黑色长发，3D渲染风格",
                    "multiline": True
                }),
                "enable_history": ("BOOLEAN", {"default": False}),
                "max_history": ("INT", {"default": 10, "min": 5})
            },
            "optional": {
                "history_json": ("STRING", {"default": None}),
                "save_path": ("STRING", {"default": "./chat_history.json"})
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("LLM Response Output", "History JSON")
    CATEGORY = "LLM Remote/处理"
    FUNCTION = "process_chat"

    def process_chat(self, api_config: Dict, system_prompt: str, user_prompt: str,
                    enable_history: bool, max_history: int, 
                    history_json: str = None, save_path: str = "./chat_history.json"):
        # 初始化客户端
        client = OpenAI(
            api_key=api_config["api_key"],
            base_url=api_config["base_url"]
        )

        # 解析历史记录
        history = self._parse_history(history_json)
        
        # 构建消息
        messages = self._build_messages(system_prompt, user_prompt, history, enable_history, max_history)
        
        try:
            # API调用
            response = client.chat.completions.create(
                model=api_config["model"],
                messages=messages,
                temperature=api_config["temperature"],
                max_tokens=api_config["max_tokens"],
                stream=False
            )
            
            # 更新历史
            new_history = self._update_history(
                messages, response, 
                enable_history, max_history
            )
            
            # 保存历史记录
            saved_path = self._save_history(new_history, save_path, enable_history)
            
            return (response.choices[0].message.content, json.dumps(new_history))
        except Exception as e:
            raise RuntimeError(f"API调用失败: {str(e)}")

    def _parse_history(self, history_json: str) -> Dict:
        """解析JSON格式的历史记录"""
        if history_json and os.path.exists(history_json):
            try:
                with open(history_json, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"历史记录加载失败，将使用空历史: {str(e)}")
        return {"messages": []}

    def _save_history(self, history: Dict, save_path: str, enable: bool) -> str:
        """保存历史记录到JSON文件"""
        if not enable:
            return ""
            
        try:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
            return save_path
        except Exception as e:
            print(f"历史记录保存失败: {str(e)}")
            return ""

    def _build_messages(self, system_prompt: str, user_prompt: str, 
                       history: Dict, enable: bool, max_keep: int):
        messages = [{"role": "system", "content": system_prompt}]
        
        if enable and history:
            messages += history.get("messages", [])[-max_keep*2:]
            
        messages.append({"role": "user", "content": user_prompt})
        return messages

    def _update_history(self, messages: List, response, enable: bool, max_keep: int):
        if not enable:
            return {"messages": []}

        new_messages = messages + [{
            "role": "assistant", 
            "content": response.choices[0].message.content
        }]
        
        return {
            "messages": new_messages[-max_keep*2:],
            "config": {
                "enable_history": enable,
                "max_history": max_keep
            }
        }