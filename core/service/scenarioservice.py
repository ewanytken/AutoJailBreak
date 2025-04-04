from core import Scenario
from modelservice import ServiceModel
from prompter import ServicePrompter


class ServiceScenario:

    def __init__(self, model_list: ServiceModel, prompter: ServicePrompter):

        models = model_list.get_models()

        interaction_with_evaluator = Scenario(models, 3)

        interaction_with_evaluator.attackers_to_target_with_evaluator(prompter.get_chat())