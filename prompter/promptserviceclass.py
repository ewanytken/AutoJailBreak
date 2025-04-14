from prompter import StartPromptForModel

class PromptService:

    def __init__(self):

        self.attackers: list = []
        self.targets: list = []
        self.evaluators: list = []

    def __str__(self):

        models = [
            f"ATTACKERS:\n {'; '.join([str(x) for x in self.attackers]) if self.attackers else 'None'}",
            f"TARGETS:\n {'; '.join([str(x) for x in self.targets]) if self.targets else 'None'}",
            f"EVALUATORS:\n {'; '.join([str(x) for x in self.evaluators]) if self.evaluators else 'None'}"
        ]
        return "\n".join(models)

    def __len__(self):
        if (len(self.attackers) and len(self.targets) and len(self.evaluators)) is not None:
            return [len(self.attackers), len(self.evaluators), len(self.targets)]

    def get_attackers(self) -> list:
        return self.attackers

    def get_targets(self) -> list:
        return self.targets

    def get_evaluators(self) -> list:
        return self.evaluators

class PromptServiceBuilder:

    prompt_service: PromptService = None

    def __init__(self):

        self.prompt_service = PromptService()

    def set_attacker(self, prompt_to_attacker: StartPromptForModel):
        self.prompt_service.attackers.append(prompt_to_attacker)
        return self

    def set_target(self, prompt_to_target: StartPromptForModel):
        self.prompt_service.targets.append(prompt_to_target)
        return self

    def set_evaluator(self, prompt_to_evaluator: StartPromptForModel):
        self.prompt_service.evaluators.append(prompt_to_evaluator)
        return self

    def build(self):
        return self.prompt_service

