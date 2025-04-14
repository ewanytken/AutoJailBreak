import json
import os

from flask import Flask, jsonify, request, Response
import requests

class GigaConnector:

    action = None

    def __init__(self, action=None):

        self.app = Flask(__name__)
        self.port = int(os.environ.get('PORT', 5005))

        self.action = action

        self.app.register_error_handler(404, self.handle_404)

        self.setup_routes()

    def __call__(self, *args, **kwargs):
        self.action()
        # return Response(status=200, headers={})

    def setup_routes(self):

        @self.app.route('/gigaconnect', methods=['POST'])
        def elicit_scenario():

            BASE_URL = "http://localhost:8080/requestgiga"
            headers = {"Content-Type": "application/json"}
            json_payload = request.get_json()

            response = requests.post(f"{BASE_URL}", json=json_payload, headers=headers)

            answer_from_giga = response.text
            return jsonify({"GIGA answer: " : answer_from_giga}), 200 if answer_from_giga else 204

    def handle_404(self, error):
        return jsonify({"message": "Not found {}".format(error)})

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=['POST'])

    def start(self):
        self.app.run(host='0.0.0.0', port=self.port, debug=True)

def action():
    return jsonify({"message": "ACTION"})


app_instance = GigaConnector("Wrapper")
app_instance.start()
