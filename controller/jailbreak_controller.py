import os

import uvicorn
from fastapi import FastAPI, Body
from core.service import ScenarioFacade, GigaRest


class JailBreakController:

    def __init__(self):
        self.app = FastAPI()
        self.register_request()

    def register_request(self):

        @self.app.post('/autojailbreak', status_code=200)
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

        @self.app.post('/external_model', status_code=200)
        def attacker_target(json = Body()):
            scenario = ScenarioFacade(json)

            return scenario.get_dialog()

        @self.app.post('/giga_model', status_code=200)
        def attacker_target(json = Body()):
            scenario = ScenarioFacade(json)

            return scenario.get_dialog()

    def start(self):
        uvicorn.run(self.app, host="127.0.0.1", port=80, log_level="info")