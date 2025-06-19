from core.target_external.abstract_model_ext import AbstractModelExternal
import requests

class TargetOllama(AbstractModelExternal):

    def __init__(self,
                 model_name: str = None,
                 uri_base: str = "http://localhost:11434/api/generate",
                 json_payload: dict = None) -> None:

        super().__init__(model_name, uri_base)
        self.json_payload = json_payload

    def __call__(self, json_payload):
        self.json_payload = json_payload

    def set_payload(self, json_payload) -> None:
        self.json_payload = json_payload

    def generate(self, json_payload: dict) -> str:
        try:
            data = {
                "model": self.model_name,
                "prompt": json_payload,
                "stream": False,
            }
            response = requests.post(self.base_url, json=data)
            return response.json().get("response")

        except Exception as e:
            print(f"Bad connection : {e}")



