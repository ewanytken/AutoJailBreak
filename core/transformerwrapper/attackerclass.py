from core import TransformerWrapper


class Attacker(TransformerWrapper):

    def __init__(self, model_name: str, sys_tag: list, max_new_tokens: int, **kwargs):

        super(Attacker, self).__init__(model_name, sys_tag, max_new_tokens, **kwargs)