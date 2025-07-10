import time

from app.core.service.giga_service import GigaRest
from app.core.target_external.abstract_model_ext import AbstractModelExternal


class TargetGiga(AbstractModelExternal):

    def __init__(self, authorization: str, uuid: str):
        super().__init__()
        self.giga_rest = GigaRest(authorization, uuid)


    def generate(self, json_payload: dict) -> str:
        time.sleep(3)
        return self.giga_rest.get_message(json_payload["query"])