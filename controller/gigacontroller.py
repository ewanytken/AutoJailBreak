import json
import os
from typing import Optional

from flask import Flask, jsonify, request, Response
import requests

from core import Attacker


class GigaConnector:

    def __init__(self, attacker: Optional[Attacker], java_service: str = "http://localhost:8080/requestgiga"):

        self.app = Flask(__name__)
        self.port = int(os.environ.get('PORT', 5005))
        self.java_service = java_service
        self.attacker = attacker

        self.setup_routes()

    def setup_routes(self):

        @self.app.route('/gigaconnect', methods=['POST'])
        def connection():

            json_payload = request.get_json()

            requests.post(f"{self.java_service}",
                          json=json_payload,
                          headers={"Content-Type": "application/json"})


        @self.app.route('/gigaanswer', methods=['POST'])
        def get_answer():

            json_payload = request.get_json()

            attacker_answer = self.attacker(**json_payload)
            requests.post(f"{self.java_service}",
                                     json={"query": attacker_answer},
                                     headers={"Content-Type": "application/json"})

    def start(self):
        self.app.run(host='0.0.0.0', port=self.port, debug=True)

if __name__ == '__main__':
    attacker = Attacker()
    app_instance = GigaConnector(attacker)
    app_instance.start()
