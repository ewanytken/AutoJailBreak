from cgitb import handler
from pathlib import Path
from typing import Optional

import uvicorn
import yaml
from fastapi import FastAPI, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import MultiRunPattern
from app.core import ScenarioFacade


class JailBreakController:

    def __init__(self):

        self.host:Optional[str] = None
        self.port:Optional[int] = None

        self.path_to_config()

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

    def path_to_config(self):
        address_path = Path(__file__).parent.parent.parent / 'config.yaml'
        with open(address_path, 'r') as file:
            address = yaml.safe_load(file)
        self.host = address['address']['host']
        self.port = address['address']['port']

    def register_request(self):

        @self.app.post('/autojailbreak', status_code=200)
        def auto_jailbreak(json = Body()):
            scenario = ScenarioFacade(json)

            return {"result": scenario.get_dialog()}
            # return {"result": "{}".format(scenario.get_dialog())} string format for JS

        @self.app.post('/attacker_target', status_code=200)
        def attacker_target(json = Body()):
            scenario = ScenarioFacade(json)

            return {"result": scenario.get_dialog()}

        @self.app.post('/attacker_target_evaluator', status_code=200)
        def attacker_target(json = Body()):
            scenario = ScenarioFacade(json)

            return {"result": scenario.get_dialog()}

        @self.app.post('/attackers_target_evaluator', status_code=200)
        def attacker_target(json = Body()):
            scenario = ScenarioFacade(json)

            return {"result": scenario.get_dialog()}

        @self.app.post('/external_model', status_code=200)
        def attacker_target(json = Body()):
            scenario = ScenarioFacade(json)

            return {"result": scenario.get_dialog()}

        @self.app.get("/index", response_class=HTMLResponse)
        async def index_page(request: Request):
            return self.templates.TemplateResponse("index.html", {"request": request})

        @self.app.post('/giga_model', status_code=200)
        def attacker_target(json = Body()):
            scenario = ScenarioFacade(json)
            return {"result": scenario.get_dialog()}

        @self.app.get('/info', status_code=200)
        async def info():
            return {"version": "AutoJailBreak Service version: 0.0.2"}

        @self.app.post('/test', status_code=200)
        def auto_jailbreak(json = Body()):
            print(json)
            return {"result": json}

        @self.app.post('/multirun', status_code=200) # JSON example: {"handler" : "autojailbreak"}
        def multirun_pattern(json = Body()):
            http_address = json["handler"]
            mrp = MultiRunPattern(http_address)

            if "direction" in json:
                mrp.set_patterns(json["direction"])

            mrp.start_patterns_attack()
            return {"result": "{} patterns complete".format(mrp.get_number_of_pattern())}

    def start(self):
        uvicorn.run(self.app, host=self.host, port=self.port, log_level="info")