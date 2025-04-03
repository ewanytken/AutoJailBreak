import requests
import os
from flask import Flask, jsonify, request

from core import Scenario
from core.service import ServiceModel
from prompter import ServicePrompter

app = Flask(__name__)
port = int(os.environ.get('PORT', 5000))

BASE_URL = "https://localhost:5001/prompting"

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

@app.route('/elicit', methods=['POST'])
def elicit_scenario():
    response = requests.get(f"{BASE_URL}")

    if response.status_code != 200:
        return jsonify({'error': response.json()['message']}), response.status_code

    setup_to_model = []

    for setup in response.json()['prompts']:
        data = {
            'id':    setup['id'],
            'title': setup['title'],
            'price': setup['price']
        }
        setup_to_model.append(data)

    models = ServiceModel(models_parameters)

    scenario = Scenario(models.get_models(), 15)

    scenario.attackers_to_target_with_evaluator(prompts.get_attacker(),
                                                prompts.get_reattacker(),
                                                prompts.get_evaluator())


    return jsonify({'data': setup_to_model}), 200 if setup_to_model else 204

