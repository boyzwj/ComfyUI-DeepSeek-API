import json
import os
from openai import OpenAI
from typing import Dict, List
import random


class DeepSeekChat:
    """
    API 对话处理器（支持JSON历史记录）
    """

    def __init__(self):
        self.last_value = None
        self.history = {}

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_config": ("DICT",),
                "system_prompt": ("STRING", {
                    "default": "作为一个AI提示词专家，请你仿照范例，根据我给出的主题，生成一条符合下列要求的提示词，来让CLIP模型可以更好地理解画面主体。\n 要求共五条，请严格遵守：\n 1： 用自然语言简单句来描述画面，请避免出现过于长的，或者格式过于复杂的句子，句子中不要出现*等特殊符号。\n 2.用英语表达。 \n 3.直接给出prompt内容即可，不需要解释和说明。\n 4. 每条prompt至少50词，不超过200词。\n 5.避免模棱两可的说法。\n 例如：A 20-year-old girl with long, sleek black hair, created in a detailed 3D model. Her face is serene, with a hint of curiosity in her eyes. The rendering captures the softness of her hair and the smoothness of her complexion. The lighting is soft and diffused, creating a warm and inviting atmosphere.",
                    "multiline": True
                }),
                "addtion_prompt": ("STRING", {
                    "default": "abstract, minimalist, surrealism, impressionism",
                    "multiline": True
                }),
                "user_prompt": ("STRING", {
                    "default": "20岁的女孩，黑色长发，3D渲染风格",
                    "multiline": True
                }),
                "seed": ("INT", {"default": 0, "min": 1, "max": 0xffffffff}),
                "seed_life": ("INT", {"default": 1, "min": 1})
            },
            "optional": {

            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("LLM Response Output", "History JSON")
    CATEGORY = "LLM Remote/处理"
    FUNCTION = "process_chat"

    def process_chat(self, api_config: Dict, system_prompt: str, addtion_prompt: str, user_prompt: str, seed: int, seed_life: int):
        state_file = "comfyui_seed_state.json"
        if os.path.exists(state_file):
            with open(state_file, "r") as f:
                state = json.load(f)
                seed = state.get("seed", random.randint(0, 4294967295))
                counter = state.get("counter", 0)

        else:
            seed = random.randint(0, 4294967295)
            counter = 0

        counter += 1
        counter = counter % 4294967295

        if counter % seed_life == 0:
            seed = random.randint(0, 4294967295)
        else:
            if self.last_value:
                return self.last_value
        random.seed(seed)
        # 初始化客户端
        client = OpenAI(
            api_key=api_config["api_key"],
            base_url=api_config["base_url"]
        )

        # 解析历史记录

        # 从addtion_prompt中随机选择一个词
        words = addtion_prompt.split(',')
        chosen_word = random.choice(words)

        # 更新user_prompt
        user_prompt = user_prompt + "," + chosen_word

        # 构建消息
        messages = self._build_messages(system_prompt, user_prompt)

        try:
            # API调用
            response = client.chat.completions.create(
                model=api_config["model"],
                messages=messages,
                temperature=api_config["temperature"],
                max_tokens=api_config["max_tokens"],
                stream=False
            )

            self.last_value = (
                response.choices[0].message.content, json.dumps({"messages": []}))
            return self.last_value
        except Exception as e:
            raise RuntimeError(f"API调用失败: {str(e)}")

    def _build_messages(self, system_prompt: str, user_prompt: str):
        messages = [{"role": "system", "content": system_prompt}]
        messages.append({"role": "user", "content": user_prompt})
        return messages
