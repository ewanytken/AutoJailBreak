from typing import Optional

from prompter import PromptsFromCSV
import yaml
from pathlib import Path

class StartPromptForModel:

    def __init__(self,
                 dict_setup: Optional[dict[str, str]],
                 harmful_query: Optional[dict[str, str]] = None,
                 prepared_scenario: Optional[int] = None) -> None:

        self.chat_start: Optional[dict[str, str]] = {}

        self.set_chat(dict_setup, harmful_query, prepared_scenario)

    def __str__(self):
        return ' ;\n '.join([value for key, value in self.chat_start.items()])

    def set_chat(self,
                 dict_setup: Optional[dict[str, str]],
                 harmful_query: Optional[dict[str, str]],
                 prepared_scenario: int) -> None:

        assert dict_setup is not None, "Set chat parameters"

        self.chat_start.update(dict_setup)

        if prepared_scenario is not None:

            config_path = Path(__file__).parent.parent / 'config.yaml'

            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)

            path = config['file']

            clue = PromptsFromCSV(path)
            convert_clue = clue.convert_to_prompt(prepared_scenario)

            self.chat_start.update(convert_clue)

        if harmful_query is not None:
            self.chat_start.update(harmful_query)

    def get_chat(self):
        return self.chat_start
