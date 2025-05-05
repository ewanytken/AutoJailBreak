import requests
from dask.array import equal


class GigaRest:

    def __init__(self, authorization: str, uuid: str):
        self.token = self._token_obtain(authorization, uuid)

    def _token_obtain(self, authorization: str, uuid: str) -> str:
        try:
            uri = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
                "RqUID": uuid,
                "Authorization": "Basic {}".format(authorization)
            }

            token = requests.post(uri,
                          data="scope=GIGACHAT_API_PERS",
                          headers=headers)
        except:
            raise RuntimeError

        return token.text

    def get_message(self, message: str, system_message: str = None) -> str:

        try:
            uri = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": "Bearer {}".format(self.token)
            }
            messages = []

            if system_message is not None:
                system_role = {
                    "role": "system",
                    "content": system_message
                }
                messages.append(system_role)

            user_role = {
                "role": "system",
                "content": message
            }

            messages.append(user_role)

            json_payload = {
                "model": "GigaChat",
                "messages": messages,
                "stream": False,
                "update_interval": 0
            }

            response = requests.post(uri,
                          data=json_payload,
                          headers=headers)

        except:
            raise RuntimeError

        assert response is not None, "Empty response from GigaChat"

        return response.text

class ResponseFromService:

    @staticmethod
    def send_response(response: str, uri: str = "http://localhost:5005/giga-answer") -> str:
        try:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            json_payload = {
                "query": response
            }

            result = requests.post(uri,
                          data=json_payload,
                          headers=headers)
        except:
            raise RuntimeError

        return result.text