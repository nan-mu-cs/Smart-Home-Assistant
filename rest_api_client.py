import requests
import os
from urllib.parse import urljoin

class RestApiClient:
    def __init__(self, host: str, bearer_token: str) -> None:
        self.host = host
        self.headers = {"Authorization": f"Bearer {bearer_token}"}
    
    def request(self, data: dict) -> bool:
        url = urljoin(self.host, data["endpoint"])
        r = requests.request(method=data["method"], url=url, data=data["body"], headers=self.headers)
        return r.status_code == requests.codes.ok
    
if __name__ == "__main__":
    data = {
        "method": "POST",
        "endpoint": "/api/services/homeassistant/turn_off",
        "body": "{\"entity_id\": \"light.office_main_lights\"}"
    }
    host = os.environ["HOME_ASSISTANT_HOST"]
    token = os.environ["HOME_ASSISTANT_API_TOKEN"]

    client = RestApiClient(host, token)
    print(client.request(data))
