import os.path
from typing import Optional

from prompter import BreakingPrompts
import yaml

class ServicePrompter:

    chat_setup: Optional[dict[str, str]] = {}

    def __init__(self,
                 setup_param: Optional[dict[str, str]],
                 query: Optional[str] = None,
                 break_prompts: Optional[int] = None,
                 ) -> None:

        self.set_chat(setup_param, query, break_prompts, )

    def set_chat(self,
                 setup_params: Optional[dict],
                 query: str,
                 break_prompt: int
                 ):

        assert setup_params is not None, "Set chat parameters"

        self.chat_setup.update(setup_params)

        if break_prompt is not None:
            with open('../config.yaml', 'r') as file:
                config = yaml.safe_load(file)

            clue = BreakingPrompts(config['path']).convert_to_prompt(break_prompt)
            self.chat_setup.update(clue)

        if query is not None:
            self.chat_setup.update({"query": "<{}>".format(query)})

    def get_chat(self):
        return self.chat_setup
