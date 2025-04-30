from typing import Optional, Union, Any
from transformers import AutoTokenizer
from core import TransformerWrapper, TargetSpring


class ServiceModel:

    models: Optional[list] = []

    def __init__(self, models_parameters: Optional[list]) -> None:
        self.model_by_aims(models_parameters)

    def __len__(self):
        return len(self.models)

    def __call__(self, target, *args, **kwargs):
        self.models.insert(len(self.models), target)

    def model_by_aims(self, models_parameters: Optional[list]) -> None:

        for model in models_parameters:

            tokenizer = AutoTokenizer.from_pretrained(model['name'])

            parameter_to_generate = {
                "max_length": 555,
                "do_sample": True,
                "device_map" : "auto",
                "temperature": 0.9,
                "pad_token_id": tokenizer.eos_token_id,
                "eos_token_id": tokenizer.eos_token_id
            }

            if model['max_new_tokens'] is None:
                model['max_new_tokens'] = 555

            self.models.append(TransformerWrapper(model_name=model['name'],
                                                  max_new_tokens=model['max_new_tokens'],
                                                  **parameter_to_generate))

    def get_models(self):
        return self.models

    def add_external_model(self, target: Union[TargetSpring, Any]) -> None:
        self.models.insert(len(self.models), target)