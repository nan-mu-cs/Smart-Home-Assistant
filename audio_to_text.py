import pyaudio
import wave
import uuid
import os
import openai


class AudioToTextWorker:
    def __init__(self) -> None:
        self.chunk = 1024
        self.channels = 2
        self.fs = 44100
        self.seconds = 3
        self.filename = ""
        self.p = pyaudio.PyAudio()
    
    def record_audio(self):
        stream = self.p.open(format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.fs,
                frames_per_buffer=self.chunk,
                input=True)
        
        frames = []

        print("start recording...")
        for i in range(0, int(self.fs / self.chunk * self.seconds)):
            data = stream.read(self.chunk)
            frames.append(data)
        print("end recording...")

        stream.stop_stream()
        stream.close()
        self.p.terminate()

        self.filename = f'{str(uuid.uuid4())}.wav'
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(frames))
        wf.close()
    
    def audio_to_text(self, delete_audio_file = True) -> str:
        assert os.path.exists(self.filename), f"Audio not exist, call record_audio function first."

        f = open(self.filename, "rb")
        transcript = openai.Audio.transcribe("whisper-1", f)

        if delete_audio_file:
            os.remove(self.filename)
            self.filename = ""
        return transcript["text"]
    
if __name__ == '__main__':
    worker = AudioToTextWorker()
    worker.record_audio()
    text = worker.audio_to_text()
    print(text)


