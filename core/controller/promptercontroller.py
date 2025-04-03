import requests
import os
from flask import Flask, jsonify, request

from prompter import ServicePrompter

app = Flask(__name__)
port = int(os.environ.get('PORT', 5001))

@app.route('/prompting', methods=['POST'])
def parameters_for_prompter():

    content = request.get_json()
    query = content['query']
    number_prompt= content['number_prompt']

    prompts = ServicePrompter(query)
    prompt_to_set = [prompts.get_attacker(),
                     prompts.get_reattacker(),
                     prompts.get_evaluator()]

    return jsonify({"prompts" : prompt_to_set})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)