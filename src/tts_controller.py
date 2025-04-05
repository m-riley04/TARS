import pyttsx3 as tts
import dotenv
from openai import OpenAI
import asyncio

class TtsController():
    def __init__(self, env_path: str = "../.env"):
        self.api_key = dotenv.get_key(dotenv_path=env_path, key_to_get="OPENAI_API_KEY")
        self.tts_engine = tts.init()
        self.client = OpenAI(api_key=self.api_key)

    def speak(self, text):
        self.tts_engine.say(text=text)
        self.tts_engine.runAndWait()