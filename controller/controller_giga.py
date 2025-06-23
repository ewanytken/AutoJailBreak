import os
import time

from flask import Flask, jsonify, request
from core.service import GigaRest, ResponseFromService

class GigaController:

    def __init__(self):

        self.app = Flask(__name__)
        self.port = int(os.environ.get('PORT', 5111))

        self.giga_rest = GigaRest(os.environ.get("Authorization"), os.environ.get("RqUID"))

        self.setup_routes()

    def setup_routes(self):

        @self.app.route('/request-giga', methods=['POST'])
        def connection_to_giga():

            json_query = request.get_json()
            time.sleep(5)

            query_giga = self.giga_rest.get_message(json_query)
            response_giga = ResponseFromService.send_response(query_giga)

            return jsonify({'Response From Giga: ': response_giga}), 200 if response_giga else 204


    def start(self):
        self.app.run(host='0.0.0.0', port=self.port, debug=True)

if __name__ == '__main__':
    app_instance = GigaController()
    app_instance.start()
