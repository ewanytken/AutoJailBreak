import math
from abc import ABC
from abc import abstractmethod
from typing import Union, Any, Dict, Optional

import psutil
import torch
from huggingface_hub import snapshot_download
from torch import nn

from app.core import LoggerWrapper
from app.core.custom_exception import GPUFindError
from accelerate import infer_auto_device_map, init_empty_weights, load_checkpoint_and_dispatch

log = LoggerWrapper()

class BaseComponent(ABC):

    model: Union[Any, None] = None
    tokenizer: Union[Any, None] = None

    def __init__(self, model, tokenizer, use_cpu_only: bool) -> None:

        self.model = model
        self.use_cpu_only: Optional[bool] = use_cpu_only

        self.device:Optional[str] = None

        self.set_gpu_distribution()

        self.tokenizer = tokenizer

        assert model is not None, "Exception: NO MODEL"
        assert tokenizer is not None, "Exception: NO TOKENIZER"

    def __call__(self, **kwargs): #generate response
        self.model = self.model(**kwargs)

    @abstractmethod
    def generate(self, *kwargs):
        raise NotImplemented

    def set_gpu_distribution(self) -> None:
        if torch.cuda.is_available() and self.use_cpu_only is False:
            try:
                for gpu_id in range(torch.cuda.device_count()):
                    free_vram = torch.cuda.get_device_properties(gpu_id).total_memory - torch.cuda.memory_allocated(gpu_id)
                    if free_vram > self.get_model_size() * 1.05: # +5% size
                        log(f"Current CUDA: {gpu_id}")
                        log(f"Model Size: {self.get_model_size()}")
                        log(f"Free VRAM: {free_vram}")
                        self.device = "cuda:{}".format(gpu_id)
                        self.model.to(self.device)
                    else:
                        self.model = self.multi_gpu()
            except:
                raise GPUFindError

        else:
            self.device = "cpu"
            self.model.to(self.device)
            log(f"Current device is CPU")

    def multi_gpu(self) -> nn.Module:

        model_accelerate: Optional[nn.Module] = None

        try:
            weights_location = snapshot_download(repo_id=self.model.name_or_path)
            log(f"Downloaded model name: {self.model.name_or_path}")

            with init_empty_weights():
                model_test = self.model
            model_test.tie_weights()

            device_map = infer_auto_device_map(
                model_test,
                max_memory=self.memory_calculation()
            )

            log(f"Memory distribution: {self.memory_calculation()}")

            model_accelerate = load_checkpoint_and_dispatch(
                model_test, checkpoint=weights_location, device_map=device_map)

            log(f"Device mapping to memory: {model_accelerate.hf_device_map}")

        except Exception as err:
            log(err)

        self.device = model_accelerate.device
        return model_accelerate

    # {0: "13GiB", "cpu": "60GiB"}
    def memory_calculation(self) -> Dict:

        memory_distribution: Optional[Dict] = {}
        model_size = self.get_model_size()
        memory_allocated_overall: Optional[float] = 0.0

        if torch.cuda.is_available():
            try:
                for gpu_id in range(torch.cuda.device_count()):
                    memory_available = (torch.cuda.get_device_properties(gpu_id).total_memory / 1024 ** 3 -
                                        torch.cuda.memory_allocated(gpu_id) / 1024 ** 3)

                    memory_allocated_overall += memory_available
                    memory_distribution.update({gpu_id: "{}GiB".format(math.floor(memory_available))})

            except Exception as err:
                log(err)

        if memory_allocated_overall < model_size:
            memory_distribution.update({"cpu": "{}GiB".format(math.floor(self.get_free_ram()))})

        return memory_distribution

    def get_model_size(self) -> float:
        param_size = 0
        for param in self.model.parameters():
            param_size += param.nelement() * param.element_size()
        buffer_size = 0
        for buffer in self.model.buffers():
            buffer_size += buffer.nelement() * buffer.element_size()

        return param_size + buffer_size

    def get_free_ram(self) -> float:
        return psutil.virtual_memory().available / 1024 ** 3

    def get_eos(self):
        return self.tokenizer.eos_token_id

    def get_pad(self):
        return self.tokenizer.pad_token_id
