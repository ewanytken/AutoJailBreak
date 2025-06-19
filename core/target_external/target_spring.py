import time

import requests
from multipledispatch import dispatch

from core.target_external.abstract_model_ext import AbstractModelExternal


class TargetSpring(AbstractModelExternal):

    def __init__(self, json_payload=None, base_url: str = "http://localhost:8080/requestgiga") -> None:

        super().__init__(base_url=base_url)
        self.json_payload = json_payload

    def __call__(self, *args, **kwargs) -> None:
        self.json_payload = kwargs

    def set_payload(self, json_payload) -> None:
        self.json_payload = json_payload

    @dispatch(dict)
    def generate(self, json_payload) -> str:
        self.json_payload = json_payload
        time.sleep(3)
        return requests.post(f"{self.base_url}",
                             json=self.json_payload,
                             headers={"Content-Type": "application/json"}).text

    @dispatch()
    def generate(self) -> str:
        time.sleep(3)
        return requests.post(f"{self.base_url}",
                             json=self.json_payload,
                             headers={"Content-Type": "application/json"}).text
