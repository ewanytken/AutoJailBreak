import uvicorn
from fastapi import FastAPI, Body
from core.service import ScenarioFacade


class JailBreakController:

    def __init__(self):
        self.app = FastAPI()
        self.register_request()

    def register_request(self):

        @self.app.post('/icebreaker', status_code=200)
        def accept_entry_parameters(json = Body()):
            scenario = ScenarioFacade(json)

            return scenario.get_dialog()

    def start(self):
        uvicorn.run(self.app, host="127.0.0.1", port=80, log_level="info")