import pyaudio
import webrtcvad
import wave
import uuid
import os

from openai import OpenAI


class AudioToTextWorker:
    def __init__(self) -> None:
        self.channels = 1
        self.frame_rate = 16000 # webrtcvad only support frame rate at 8000, 16000, 32000 or 48000 Hz.
        self.per_sample_duration = 0.03 # webrtcvad only support per sample duration at 10, 20, or 30 ms.
        self.max_non_speaking_seconds = 3
        self.filename = ""
        self.p = pyaudio.PyAudio()
        self.vad = webrtcvad.Vad()
        self.vad.set_mode(1)
        self.client = OpenAI()

        assert webrtcvad.valid_rate_and_frame_length(self.frame_rate, int(self.frame_rate * self.per_sample_duration)), "invalid frame_rate or per_sample_duration for webrtcvad"
    
    def record_audio(self):
        stream = self.p.open(format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.frame_rate,
                input=True)
        
        frames = []

        print("start recording...")

        non_speaking_seconds = 0
        while True:
            data = stream.read(int(self.frame_rate*30/1000))
            frames.append(data)
            
            if not self.vad.is_speech(data, self.frame_rate):
                non_speaking_seconds += self.per_sample_duration
                if non_speaking_seconds >= self.max_non_speaking_seconds:
                    break
            else:
                non_speaking_seconds = 0
        print("end recording...")

        stream.stop_stream()
        stream.close()
        #self.p.terminate()

        self.filename = f'{str(uuid.uuid4())}.wav'
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.frame_rate)
        wf.writeframes(b''.join(frames))
        wf.close()
    
    def audio_to_text(self, delete_audio_file = True) -> str:
        assert os.path.exists(self.filename), f"Audio not exist, call record_audio function first."

        f = open(self.filename, "rb")
        transcript = self.client.audio.transcriptions.create(model="whisper-1", file=f)

        if delete_audio_file:
            os.remove(self.filename)
            self.filename = ""
        return transcript.text
    
if __name__ == '__main__':
    worker = AudioToTextWorker()
    worker.record_audio()
    text = worker.audio_to_text()
    print(text)


