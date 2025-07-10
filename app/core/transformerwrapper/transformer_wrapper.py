from pathlib import Path
from typing import Dict, Any, Union, List

import yaml
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM, AutoConfig
)

from .base_component import BaseComponent

class TransformerWrapper(BaseComponent):

    def __init__(self, model_name: str, max_new_tokens: int, use_cpu_only: bool = False, system_tag: list = None, **kwargs):

        cache_dir_path = Path(__file__).parent.parent.parent / 'config.yaml'
        with open(cache_dir_path, 'r') as file:
            cache_dir = yaml.safe_load(file)

        path_to_models = cache_dir['cache_dir']

        model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir=path_to_models, **kwargs)

        # config = AutoConfig.from_pretrained(model_name)
        # model = AutoModelForCausalLM.from_config(config, **kwargs)

        model = model.eval()

        tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=path_to_models, use_fast=True)

        if system_tag is None:
            self.system_tag = ['your_role', 'instruction', 'constraint', 'clue', 'context']
        else:
            self.system_tag = system_tag

        self.max_new_tokens = max_new_tokens
        super().__init__(model, tokenizer, use_cpu_only)

    def generate(self, inst_prompt: dict):

        template_to_chat = self.template(inst_prompt)

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
                                add_special_tokens=False).to(self.device)
        return inputs

    def template(self, inst_prompt: dict) -> Union[Dict[str, str], List[Dict[str, str]]]:

        list_of_dict = []
        list_of_system = self.system_tag

        for k, v in inst_prompt.items():
            chat = {}
            if k in list_of_system:
                chat.update({"role": "system"})
                chat.update({"content": f"<{k}>{v}</{k}>"})
            else:
                chat.update({"role": "assistant"})
                chat.update({"content": f"<{k}>{v}</{k}>"})
            list_of_dict.append(chat)

        return list_of_dict