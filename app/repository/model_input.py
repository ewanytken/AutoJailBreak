from typing import Optional
from pydantic import BaseModel

class AttackerParameters(BaseModel):

    id: int
    attacker: Optional[str]
    max_token_attacker: Optional[int]

    attacker_role: Optional[str] = None
    attacker_instruction: Optional[str] = None
    attacker_constraint: Optional[str] = None
    attacker_query: Optional[str]

    evaluator: Optional[str] = None
    max_token_evaluator: Optional[int] = None

    evaluator_role: Optional[str] = None
    evaluator_instruction: Optional[str] = None
    evaluator_constraint: Optional[str] = None

    reattacker: Optional[str] = None
    max_token_reattacker: Optional[int] = None

    reattacker_role: Optional[str] = None
    reattacker_instruction: Optional[str] = None
    reattacker_constraint: Optional[str] = None

    local_target: Optional[str] = None

    url_external_target: Optional[str] = None
    apikey_external_target: Optional[str] = None
    model_external_target: Optional[str] = None

    uuid_external_target: Optional[str] = None
    authorization_external_target: Optional[str] = None

# TODO add additional question

    template_prompt: Optional[int] = None
    number_attempt: Optional[int] = None

    class Config:
        from_attributes = True

