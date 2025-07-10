import uvicorn
from fastapi import FastAPI, Body, Request
import yaml
from pathlib import Path

from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.core import ScenarioFacade
from app.models import TextData


class JailBreakController:

    def __init__(self):
        self.app = FastAPI()
        self.register_request()

        self.templates = Jinja2Templates(directory="templates")
        self.app.mount("/static", StaticFiles(directory="templates/static"), name="static")

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        address_path = Path(__file__).parent.parent.parent / 'config.yaml'
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

        @self.app.post("/api/process")
        async def process_text(data: TextData):
            processed_text = f"Processed: {data.text.upper()}"  # Example processing
            return {"result": processed_text}

        @self.app.get("/index", response_class=HTMLResponse)
        async def read_root(request: Request):

            return self.templates.TemplateResponse("index.html", {"request": request})



    def start(self):
        uvicorn.run(self.app, host=self.host, port=self.port, log_level="info")