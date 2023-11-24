import json

from typing import Union
from openai import OpenAI


class ChatApiClient:
    def __init__(self, system_prompts: str, model: str = "gpt-4"):
        self.system_prompts = system_prompts
        self.model = model
        self.client = OpenAI()
    
    def chat(self, prompt: str) -> Union[dict, str]:
        response = self.client.chat.completions.create(
            model=self.model,
            messages = [
                {"role": "system", "content": self.system_prompts},
                {"role": "user", "content": prompt},
            ]
        )
        text = response.choices[0].message.content
        try:
            return json.loads(text)
        except json.decoder.JSONDecodeError:
            return text

if __name__ == "__main__":
    with open("./system_prompts.txt", "r") as file:
        system_prompts = []
        for line in file:
            system_prompts.append(line)
        system_prompts = "\n".join(system_prompts)

        client = ChatApiClient(system_prompts)

        print(client.chat("turn off office light"))
