from abc import ABC
from abc import abstractmethod
from typing import Union, Any
import torch.nn as nn
import torch


class BaseComponent(ABC):

    model: Union[Any, None] = None
    tokenizer: Union[Any, None] = None

    def __init__(self, model, tokenizer, use_cpu: bool, device: str = 'cpu'):
        if torch.cuda.is_available() and use_cpu is False:
            device = "cuda"

        if torch.cuda.device_count() > 1:
            print(f"Using {torch.cuda.device_count()} GPUs!")
            self.model = nn.DataParallel(model)

        self.model = model.to(device)

        self.tokenizer = tokenizer
        self.device = device

        assert model is not None, "Exception: NO MODEL"
        assert tokenizer is not None, "Exception: NO TOKENIZER"

    def __call__(self, **kwargs): #generate response
        self.model = self.model(**kwargs)

    def set_eos(self):
        return self.tokenizer.eos_token_id

    def set_pad(self):
        return self.tokenizer.pad_token_id

    @abstractmethod
    def generate(self, *kwargs):
        raise NotImplemented