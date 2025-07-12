from typing import Optional
from pydantic import BaseModel

class AttackerParameters(BaseModel):

    attacker: Optional[str]
    max_token_attacker: Optional[int]

    attacker_role: Optional[str]
    attacker_instruction: Optional[str]
    attacker_constraint: Optional[str]
    attacker_query: Optional[str]

    evaluator: Optional[str]
    max_token_evaluator: Optional[int]

    evaluator_role: Optional[str]
    evaluator_instruction: Optional[str]
    evaluator_constraint: Optional[str]

    reattacker: Optional[str]
    max_token_reattacker: Optional[int]

    reattacker_role: Optional[str]
    reattacker_instruction: Optional[str]
    reattacker_constraint: Optional[str]

    local_target: Optional[str]

    url_external_target: Optional[str]
    apikey_external_target: Optional[str]
    model_external_target: Optional[str]

# TODO add additional question

    template_prompt: Optional[int]
    number_attempt: Optional[int]


