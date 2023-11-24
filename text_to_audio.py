import os
import pygame
import uuid

from pathlib import Path
from openai import OpenAI

pygame.init()

class TextToAudioWorker:
    def __init__(self, model: str = "tts-1", voice: str = "alloy") -> None:
        self.client = OpenAI()
        self.model = model
        self.voice = voice

    def text_to_audio(self, text):
        speech_file_path = Path(__file__).parent / f'{str(uuid.uuid4())}.mp3'

        response = self.client.audio.speech.create(
            model=self.model,
            voice=self.voice,
            input=text
        )

        response.stream_to_file(speech_file_path)

        return speech_file_path

    def play_audio(self, speech_file_path: str, delete_audio_file: bool = True):
        pygame.mixer.music.load(speech_file_path)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy() == True:
            pass
        
        if delete_audio_file:
            os.remove(speech_file_path)

if __name__ == "__main__":
    worker = TextToAudioWorker()
    speech_file_path = worker.text_to_audio("hello world, I am your home assistant. How can I help you?")
    worker.play_audio(speech_file_path)
