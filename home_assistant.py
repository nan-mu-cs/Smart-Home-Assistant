import os
import time

from audio_to_text import AudioToTextWorker
from chat_api_client import ChatApiClient
from rest_api_client import RestApiClient

class HomeAssistant:
    def __init__(self) -> None:
        self.read_environ()
        self.read_system_prompts()

        self.audio_to_text_worker = AudioToTextWorker()
        self.chat_api_client = ChatApiClient(self.system_prompts)
        self.rest_api_client = RestApiClient(self.home_assistant_host, self.home_assistant_token)

    def read_environ(self):
        self.home_assistant_host = os.environ["HOME_ASSISTANT_HOST"]
        if not self.home_assistant_host:
            raise KeyError("HOME_ASSISTANT_HOST not set")

        self.home_assistant_token = os.environ["HOME_ASSISTANT_API_TOKEN"]
        if not self.home_assistant_token:
            raise KeyError("HOME_ASSISTANT_API_TOKEN not set")
        
        if not os.environ["OPENAI_API_KEY"]:
            raise KeyError("OPENAI_API_KEY not set")

    def read_system_prompts(self, path: str = "./system_prompts.txt"):
        with open("./system_prompts.txt", "r") as file:
            system_prompts = []
            for line in file:
                system_prompts.append(line)
            self.system_prompts = "\n".join(system_prompts)

    def run(self):
        while True:
            self.audio_to_text_worker.record_audio()
            prompt = self.audio_to_text_worker.audio_to_text()
            print(f"User: {prompt}")
            
            if "Bye-bye" in prompt or not prompt:
                break

            reply = self.chat_api_client.chat(prompt)
            if isinstance(reply, str):
                print(f"Assistant: {reply}")
                continue

            status = self.rest_api_client.request(reply)
            if status:
                print(f"Assistant: Task Done.")
            else:
                print(f"Assistant: Task Failed.")

            time.sleep(2)

if __name__ == "__main__":
    home_assistant = HomeAssistant()
    home_assistant.run()

