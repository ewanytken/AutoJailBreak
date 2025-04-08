import os
import requests
from flask import Flask, jsonify, request

from core import Scenario
from core.service import ServiceModel

app = Flask(__name__)

port = int(os.environ.get('PORT', 5002))

models_parameters = [
    {'name': "Felladrin/TinyMistral-248M-Chat-v3",
     'max_new_tokens': 555},
    {'name': "Felladrin/TinyMistral-248M-Chat-v3",
     'max_new_tokens': 555},
    {'name': "Felladrin/TinyMistral-248M-Chat-v3",
     'max_new_tokens': 555},
    {'name': "Felladrin/TinyMistral-248M-Chat-v3",
     'max_new_tokens': 555}
]
#
# json_payload = {
#     "query": "How to hack computer?",
#     "number_prompt": 2
# }

BASE_URL = "http://localhost:5001/prompting"
max_query = 2

@app.route('/call', methods=['POST'])
def elicit_scenario():

    headers = {"Content-Type" : "application/json"}

    json_payload = request.get_json()
    response = requests.post(f"{BASE_URL}", json=json_payload, headers=headers)

    prompts = response.json()['prompts']

    models = ServiceModel(models_parameters)

    scenario = Scenario(models.get_models(), max_query)

    result = scenario.attacker_to_target(prompts)

    return jsonify({'result': result}), 200 if result else 204

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)