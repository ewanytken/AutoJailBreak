import time

from core.service import GigaRest
from core.target_external import AbstractModelExternal


class TargetGiga(AbstractModelExternal):

    def __init__(self, authorization: str, uuid: str):
        super().__init__()
        self.giga_rest = GigaRest(authorization, uuid)


    def generate(self, json_payload: dict) -> str:
        time.sleep(3)
        return self.giga_rest.get_message(json_payload["query"])