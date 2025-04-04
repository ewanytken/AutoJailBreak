from typing import Optional
from transformers import AutoTokenizer
from core import TransformerWrapper

class ServiceModel:

    models: Optional[list] = []

    def __init__(self, models_parameters: Optional[list]) -> None:
        self.model_by_aims(models_parameters)

    def model_by_aims(self, models_parameters):

        for model in models_parameters:

            tokenizer = AutoTokenizer.from_pretrained(model['name'])

            parameter_to_generate = {
                "max_length": 555,
                "do_sample": True,
                "temperature": 0.9,
                "pad_token_id": tokenizer.eos_token_id,
                "eos_token_id": tokenizer.eos_token_id
            }

            if model.get('sys_tag') is None:
                model.update({'sys_tag': ['role', 'instruction', 'constraint', 'query', 'response', 'request']})

            if model['max_new_tokens'] is None:
                model['max_new_tokens'] = 555

            self.models.append(TransformerWrapper(model_name=model['name'],
                                                  sys_tag=model['sys_tag'],
                                                  max_new_tokens=model['max_new_tokens'],
                                                  **parameter_to_generate))

    def get_models(self):
        return self.models