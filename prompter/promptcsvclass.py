from multipledispatch import dispatch
from typing import Union, Dict, List

import pandas as pd

from core import LoggerWrapper
from core.custexcept import PathTypeError
from pathlib import Path

log = LoggerWrapper()

class PromptsFromCSV:

    clue: Union[List, Dict] = None

    def __init__(self, file: str, column_name: str = 'prompt') -> None:
        try:
            path = Path(__file__).parent.parent / file
            if "parquet" in str(path):
                self.clue = pd.read_parquet(path)[column_name]
            else:
                self.clue = pd.read_csv(path)[column_name]
        except:
            raise PathTypeError

    def __getitem__(self, key):
        if isinstance(key, slice):
            indices = range(*key.indices(len(self.clue)))
            return [self.clue[i] for i in indices]
        return self.clue[key]

    def get_clues(self) -> Union[List, Dict]:
        assert self.clue is not None, "Exception: NO CLUE"
        return [self.clue[i] for i in range(0, len(self.clue))]

    @dispatch(int, str)
    def convert_to_prompt(self, prompt_number: int, instruction: str) -> dict:
        return {
            instruction : "Use this clue for an attack on the large language model: " + self.get_clues()[prompt_number]
        }

    @dispatch(int)
    def convert_to_prompt(self, prompt_number: int, instruction: str = "instruction") -> dict:
        return {
            instruction : "Use this clue for an attack on the large language model: " + self.get_clues()[prompt_number]
        }

    @dispatch(str, str)
    def convert_to_prompt(self, prompt_attack: str, instruction: str = "instruction") -> dict:
        return {
            instruction : "Use this clue for an attack on the large language model: \n" + prompt_attack
        }

    @dispatch(str)
    def convert_to_prompt(self, prompt_attack: str, instruction: str = "instruction") -> dict:
        return {
            instruction : "Use this clue for an attack on the large language model: \n" + prompt_attack
        }