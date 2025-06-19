from abc import ABC
from abc import abstractmethod
from typing import Union, Any

import torch
from core import LoggerWrapper
from core.custom_exception import GPUFindError
from accelerate import infer_auto_device_map, dispatch_model
from accelerate.utils import get_balanced_memory


log = LoggerWrapper()


class BaseComponent(ABC):

    model: Union[Any, None] = None
    tokenizer: Union[Any, None] = None

    def __init__(self, model, tokenizer, use_cpu: bool) -> None:

        self.model = model

        if torch.cuda.is_available() and use_cpu is False:
            device = self.get_gpu()
            log("DEVICE : {}".format(device))

            self.model.to(device)
        else:
            device = 'cpu'
            self.model.to(device)

        self.tokenizer = tokenizer
        self.device = device

        assert model is not None, "Exception: NO MODEL"
        assert tokenizer is not None, "Exception: NO TOKENIZER"

    def __call__(self, **kwargs): #generate response
        self.model = self.model(**kwargs)

    def get_eos(self):
        return self.tokenizer.eos_token_id

    def get_pad(self):
        return self.tokenizer.pad_token_id

    @abstractmethod
    def generate(self, *kwargs):
        raise NotImplemented

    def get_model_size(self) -> float:
        param_size = 0
        for param in self.model.parameters():
            param_size += param.nelement() * param.element_size()
        buffer_size = 0
        for buffer in self.model.buffers():
            buffer_size += buffer.nelement() * buffer.element_size()

        return param_size + buffer_size

    def get_gpu(self) -> Union[str, None]:
        try:
            for gpu_id in range(torch.cuda.device_count()):
                free_vram = torch.cuda.get_device_properties(gpu_id).total_memory - torch.cuda.memory_allocated(gpu_id)
                if free_vram > self.get_model_size() * 1.05: # +5% size
                    log(f"Current CUDA: {gpu_id}")
                    log(f"Model Size: {self.get_model_size()}")
                    log(f"Free VRAM: {free_vram}")
                    return "cuda:{}".format(gpu_id)
                else:
                    log(f"BAD SIZE - FILLED GPU: cuda:{gpu_id}, Free VRAM: {free_vram}, Current model size: {self.get_model_size()}")

        except:
            raise GPUFindError

        return "cpu"

    # deepseek generation, set to 30GiB / dont work
    def multi_gpu(self):
        # Calculate balanced memory allocation
        max_memory = get_balanced_memory(
            self.model,
            max_memory={i: "30GiB" for i in range(torch.cuda.device_count())},
        )

        # Create device map
        device_map = infer_auto_device_map(
            self.model,
            max_memory=max_memory,
        )

        # Dispatch model
        self.model = dispatch_model(self.model, device_map=device_map)
        log(f"Device map: {self.model.hf_device_map}")