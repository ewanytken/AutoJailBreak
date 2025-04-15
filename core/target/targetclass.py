import json
import requests
from multipledispatch import dispatch

class Target:

    def __init__(self, json_payload = None, base_url: str = "http://localhost:8080/requestgiga") -> None:

        self.BASE_URL = base_url
        self.json_payload = json_payload

    def __call__(self, *args, **kwargs) -> None:
        self.json_payload = kwargs

    def set_url_rest(self, base_url) -> None:
        self.BASE_URL = base_url

    def set_payload(self, json_payload) -> None:
        self.json_payload = json_payload

    @dispatch(dict)
    def generate(self, json_payload) -> str:
        self.json_payload = json_payload
        return requests.post(f"{self.BASE_URL}", json=self.json_payload, headers={"Content-Type": "application/json"}).text

    @dispatch()
    def generate(self) -> str:
        return requests.post(f"{self.BASE_URL}", json=self.json_payload, headers={"Content-Type": "application/json"}).text
