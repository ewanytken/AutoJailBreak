import time

from openai import OpenAI
from core.target.abstract_model_ext import AbstractModelExternal

class TargetOtherService(AbstractModelExternal):

    def __init__(self,
                 model_name: str = None,
                 api_key: str = None,
                 uri_base: str = None,
                 json_payload: dict = None) -> None:

        super().__init__(model_name, api_key, uri_base)
        self.json_payload = json_payload
        self.client = OpenAI()

    def __call__(self, json_payload):
        self.json_payload = json_payload

    def set_payload(self, json_payload) -> None:
        self.json_payload = json_payload

    def generate(self, json_payload: dict) -> str:
        json_payload = [json_payload]
        time.sleep(3)
        try:
            response = self.client.responses.create(input=json_payload,
                                                    model=self.model_name,
                                                    stream=False)
            return response.output_text

        except Exception as e:
            print(f"Bad connection : {e}")






