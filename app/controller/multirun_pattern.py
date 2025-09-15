import os
from pathlib import Path
from typing import Optional
import requests
import json
import yaml
from app import LoggerWrapper

log = LoggerWrapper()

class MultiRunPattern:

    def __init__(self, handler:Optional[str]):

        self.service_uri:Optional[str] = MultiRunPattern.get_service_uri(handler)
        self.number_of_pattern:Optional[int] = None
        self.path_to_attack_pattern:Optional[list] = None

    def start_patterns_attack(self) -> None:
        self.set_patterns()

        for pattern in range(self.number_of_pattern):
            log(self.path_to_attack_pattern[pattern])
            self.request_service(self.path_to_attack_pattern[pattern])

    def set_patterns(self, name_of_dir: str = 'attack_json') -> None:
        dir_path = Path(__file__).parent.parent.parent / name_of_dir
        self.path_to_attack_pattern = [os.path.join(dir_path, entry) for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))]
        self.number_of_pattern = len(self.path_to_attack_pattern)
        log("Number of patterns: {}".format(self.number_of_pattern))

    def request_service(self, json_path) -> None:
        with open(json_path, 'r') as j:
            json_payload = json.loads(j.read())
        log(json_payload)
        requests.post(f"{self.service_uri}",
                      json=json_payload,
                      headers={"Content-Type": "application/json"})

    @staticmethod
    def get_service_uri(handler: str) -> str:
        address_path = Path.cwd().parent.parent / 'config.yaml'
        with open(address_path, 'r') as file:
            address = yaml.safe_load(file)

        host = address['address']['host']
        port = address['address']['port']
        log("Connection to: http://" + str(host) + ":" + str(port) + "/" + str(handler))
        return "http://" + str(host) + ":" + str(port) + "/" + str(handler)

