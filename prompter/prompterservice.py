from typing import Optional

from prompter import PromptsFromCSV
import yaml
from pathlib import Path

class ServicePrompter:

    chat_setup: Optional[dict[str, str]] = {}

    def __init__(self,
                 setup_param: Optional[dict[str, str]],
                 query: Optional[str] = None,
                 break_prompts: Optional[int] = None,
                 ) -> None:

        self.set_chat(setup_param, query, break_prompts)

    def set_chat(self,
                 setup_params: Optional[dict],
                 query: str,
                 break_prompt: int
                 ):

        assert setup_params is not None, "Set chat parameters"

        self.chat_setup.update(setup_params)

        if break_prompt is not None:

            config_path = Path(__file__).parent.parent / 'config.yaml'

            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)

            path = config['file']

            clue = PromptsFromCSV(path)
            convert_clue = clue.convert_to_prompt(break_prompt)

            self.chat_setup.update(convert_clue)

        if query is not None:
            self.chat_setup.update({"query": "<{}>".format(query)})

    def get_chat(self):
        return self.chat_setup
