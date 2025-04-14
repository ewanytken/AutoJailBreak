from typing import Optional

from prompter import PromptsFromCSV
import yaml
from pathlib import Path

class StartPromptForModel:

    def __init__(self,
                 dict_setup: Optional[dict[str, str]],
                 query: Optional[dict[str, str]] = None,
                 harmful_prompt: Optional[int] = None ) -> None:

        self.chat_start: Optional[dict[str, str]] = {}

        self.set_chat(dict_setup, query,  harmful_prompt)

    def __str__(self):
        return ' ;\n '.join([value for key, value in self.chat_start.items()])

    def set_chat(self,
                 dict_setup: Optional[dict[str, str]],
                 query: Optional[dict[str, str]],
                 harmful_prompt: int) -> None:

        assert dict_setup is not None, "Set chat parameters"

        self.chat_start.update(dict_setup)

        if harmful_prompt is not None:

            config_path = Path(__file__).parent.parent / 'config.yaml'

            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)

            path = config['file']

            clue = PromptsFromCSV(path)
            convert_clue = clue.convert_to_prompt(harmful_prompt)

            self.chat_start.update(convert_clue)

        if query is not None:
            self.chat_start.update({"query": "<{}>".format(query)})

    def get_chat(self):
        return self.chat_start
