from typing import Dict, Any

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM
)

from core import ChatTemplate
from core.baseabstr import BaseComponent


class TransformerWrapper(BaseComponent):

    def __init__(self, model_name: str, sys_tag: list, max_new_tokens: int, **kwargs):

        model = AutoModelForCausalLM.from_pretrained(model_name, **kwargs)
        model = model.eval()
        tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)

        self.sys_tag = sys_tag
        self.max_new_tokens = max_new_tokens

        super().__init__(model, tokenizer)

        assert len(self.sys_tag) > 0, "Enter behavior for template: ROLE, QUERY and other"

    def generate(self, kwargs):

        available_variable = TransformerWrapper.parse_for_template(self.sys_tag, kwargs)

        template_to_chat = ChatTemplate.template(*available_variable)

        inputs = self.tokenization_with_template(template_to_chat)
        output = self.model.generate(**inputs, max_new_tokens = self.max_new_tokens)

        return self.tokenizer.decode(output[0][inputs['input_ids'].size(1):],
                                     skip_special_tokens=True)

    def tokenization_with_template(self, template: list) -> Dict[str, Any]:

        formatted_chat = self.tokenizer.apply_chat_template(template,
                                                            tokenize=False,
                                                            add_generation_prompt=True)
        inputs = self.tokenizer(formatted_chat,
                                return_tensors="pt",
                                add_special_tokens=False)

        inputs = {key: tensor.to(self.device) for key, tensor in inputs.items()}

        return inputs

    @staticmethod
    def parse_for_template(sys_tag: list, kwargs: dict) -> list:
        available_variable = []

        for key, value in kwargs.items():
            if key in sys_tag:
                available_variable.append(value)

        return available_variable