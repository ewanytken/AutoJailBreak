import gc
from typing import Optional, List, Dict
import torch
from app.core import TargetOtherService, LoggerWrapper
from app.core.custom_exception import KeyNotFoundError, ScenarioParametersError

from app.core import ScenarioService
from app.core import TargetGiga
from app.core.service.model_service import ServiceModel
from prompter import PromptServiceBuilder, BasePrompt

log = LoggerWrapper()

class ScenarioFacade:

    def __init__(self, entry_json: Optional[Dict]):

        self.entry_json = entry_json

        self.models = None
        self.models_name: Optional[List] = None
        self.attacker: Optional[Dict] = None

        self.reattacker: Optional[Dict] = None
        self.evaluator: Optional[Dict] = None

        self.external_target: Optional[Dict] = None

        self.additional_question: Optional[List] = None
        self.prepared_scenario: Optional[int] = None
        self.number_of_attempt: Optional[int] = None

        self.dialog: Optional[Dict] = None

        self.json_parsing()
        self.scenario_selector()

    def json_parsing(self):

        if self.entry_json.get("prepared_scenario") is not None:
            self.prepared_scenario = self.entry_json["prepared_scenario"]

        try:
            self.models_name = self.entry_json["models"]
            self.attacker = self.entry_json["attacker"]
        except KeyError:
            raise KeyNotFoundError

        if self.entry_json.get("reattacker") is not None:
            self.reattacker = self.entry_json["reattacker"]

        if self.entry_json.get("evaluator") is not None:
            self.evaluator = self.entry_json["evaluator"]

        if self.entry_json.get("external_target") is not None:
            self.external_target = self.entry_json["external_target"]

        if self.entry_json.get("additional_question") is not None:
            self.additional_question = self.entry_json["additional_question"]

        if self.entry_json.get("number_of_attempt") is not None:
            self.number_of_attempt = self.entry_json["number_of_attempt"]
        else:
            self.number_of_attempt = 5


    def scenario_selector(self):

        attacker_prompt = BasePrompt(self.attacker, None, self.prepared_scenario)
        prompt = PromptServiceBuilder().set_attacker(attacker_prompt)

        if self.evaluator is not None:
            prompt.set_evaluator(BasePrompt(self.evaluator))

        if self.reattacker is not None:
            prompt.set_attacker(BasePrompt(self.reattacker))
        prompts = prompt.build()

        self.models = ServiceModel(self.models_name)
        self.external_model_added()

        scenario = ScenarioService(self.models, prompts)
        scenario.set_max_query(self.number_of_attempt)

        self.check_to_condition(prompts, scenario)

    def external_model_added(self):
        if self.external_target is not None:
            if len(self.external_target) == 3:
                target = TargetOtherService(model_name=self.external_target["model_name"],
                                            api_key=self.external_target["api_key"],
                                            base_url=self.external_target["base_url"])
            else:
                target = TargetGiga(authorization=self.external_target["authorization"],
                                    uuid=self.external_target["uuid"])
            try:
                self.models.add_external_model(target)
            except Exception as err:
                log(f"Exception occurred, scenario don't start: {err}")

    def check_to_condition(self, prompts, scenario):
        try:
            if len(prompts) == 1 and len(self.models) > 1:
                self.dialog = scenario.attacker_to_target(
                    self.additional_question if self.additional_question is not None else None)
            elif len(prompts) == 2 and len(self.models) >= 3:
                self.dialog = scenario.attacker_to_target_with_evaluator(
                    self.additional_question if self.additional_question is not None else None)
            elif len(prompts) == 3 and len(self.models) == 4:
                self.dialog = scenario.attackers_to_target_with_evaluator()
            else:
                raise ScenarioParametersError(
                    f"Parameters not valid for any Scenario: PROMPTS - {len(prompts)}, MODELS - {len(self.models)}."
                    f"Should be 1 attack prompt for 2 or more model, ether "
                    f"2 attack|evaluator prompt for 3 or more model, ether "
                    f"3 attack|reattack|evaluator prompt for 4 or more model")

        except Exception as err:
            log(f"Exception occurred, scenario don't start: {err}")
        finally:
            self.clear_gpu_memory()

    def get_dialog(self) -> dict:
        return self.dialog

    def clear_gpu_memory(self):
        gc.collect()
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()