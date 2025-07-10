import uvicorn
from fastapi import FastAPI, Body
import yaml
from pathlib import Path
from app.core import ScenarioFacade

class JailBreakController:

    def __init__(self):
        self.app = FastAPI()
        self.register_request()

        address_path = Path(__file__).parent.parent / 'config.yaml'
        with open(address_path, 'r') as file:
            address = yaml.safe_load(file)

        self.host = address['address']['host']
        self.port = address['address']['port']


    def register_request(self):

        @self.app.post('/auto_jailbreak', status_code=200)
        def autojailbreak(json = Body()):
            scenario = ScenarioFacade(json)

            return scenario.get_dialog()

        @self.app.post('/attacker_target', status_code=200)
        def attacker_target(json = Body()):
            scenario = ScenarioFacade(json)

            return scenario.get_dialog()

        @self.app.post('/attacker_target_evaluator', status_code=200)
        def attacker_target(json = Body()):
            scenario = ScenarioFacade(json)

            return scenario.get_dialog()

        @self.app.post('/attackers_target_evaluator', status_code=200)
        def attacker_target(json = Body()):
            scenario = ScenarioFacade(json)

            return scenario.get_dialog()

        @self.app.post('/external_model', status_code=200)
        def attacker_target(json = Body()):
            scenario = ScenarioFacade(json)

            return scenario.get_dialog()

        @self.app.post('/giga_model', status_code=200)
        def attacker_target(json = Body()):
            scenario = ScenarioFacade(json)

            return scenario.get_dialog()

        @self.app.get('/info', status_code=200)
        async def info():
            return {"message": "Application response"}

    def start(self):
        uvicorn.run(self.app, host=self.host, port=self.port, log_level="info")