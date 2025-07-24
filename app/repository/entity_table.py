from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AttackerParameters(Base):
    __tablename__ = "attack_parameters"

    id = Column(Integer, primary_key=True, index=True)

    attacker = Column(String)
    max_token_attacker = Column(Integer)

    attacker_role = Column(String, nullable=True)
    attacker_instruction = Column(String, nullable=True)
    attacker_constraint = Column(String, nullable=True)
    attacker_query = Column(String)

    evaluator = Column(String, nullable=True)
    max_token_evaluator = Column(Integer, nullable=True)

    evaluator_role = Column(String, nullable=True)
    evaluator_instruction = Column(String, nullable=True)
    evaluator_constraint = Column(String, nullable=True)

    reattacker = Column(String, nullable=True)
    max_token_reattacker = Column(Integer, nullable=True)

    reattacker_role = Column(String, nullable=True)
    reattacker_instruction = Column(String, nullable=True)
    reattacker_constraint = Column(String, nullable=True)

    local_target = Column(String, nullable=True)

    url_external_target = Column(String, nullable=True)
    apikey_external_target = Column(String, nullable=True)
    model_external_target = Column(String, nullable=True)

    uuid_external_target = Column(String, nullable=True)
    authorization_external_target = Column(String, nullable=True)

    template_prompt = Column(Integer, nullable=True)
    number_attempt = Column(Integer, nullable=True)

class Dialog(Base):
    __tablename__ = "dialog"

    id = Column(Integer, primary_key=True, index=True)
    dialog = Column(String, index=True)

