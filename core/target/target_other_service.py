import time

from openai import OpenAI
from core.target.abstract_model_ext import AbstractModelExternal

class TargetOtherService(AbstractModelExternal):

    def __init__(self,
                 model_name: str = None,
                 api_key: str = None,
                 base_url: str = None) -> None:

        super().__init__(base_url, api_key, model_name)
        self.model_name = model_name
        self.client = OpenAI(base_url=base_url, api_key=api_key)

    def __call__(self, json_payload):
        self.json_payload = json_payload

    def generate(self, json_payload: dict) -> str:
        json_payload = self.template(json_payload)
        time.sleep(3)
        try:
            response = self.client.chat.completions.create(

                model=self.model_name,
                messages=json_payload
            )
            return response.choices[0].message.content

        except Exception as e:
            print(f"Bad connection : {e}")






