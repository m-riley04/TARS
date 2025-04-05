import pyttsx3 as tts
import dotenv
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

class TtsController():
    def __init__(self, env_path: str = "../.env"):
        self.api_key = dotenv.get_key(dotenv_path=env_path, key_to_get="OPENAI_API_KEY")
        self.tts_engine = tts.init()
        self.client = AsyncOpenAI(api_key=self.api_key)
        
        # Set voice properties
        self.tone = "Sincere, lighthearted, neutral."
        self.voice_affect = "Calm, composed, but witty. Competent and in control, instilling trust."
        self.pacing = "Constant throughout."
        self.emotion = "Calm, helpful."
        self.pronunciation = "Clear, precise: Ensures clarity, especially with key details."
        self.pauses = "Short pauses just before finishing sentences, almost like a punchline."

    async def speak(self, text):
        async with self.client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="onyx",
            input=text,
            instructions=f"Voice Affect: {self.voice_affect}\nTone: {self.tone}\nPacing: {self.pacing}",
            response_format="pcm"
        ) as response:
            await LocalAudioPlayer().play(response)

async def main():
    # Init .env file
    import dotenv
    dotenv.load_dotenv(dotenv.find_dotenv())
    
    tts_controller = TtsController()
    text = "Everybody good? Plenty of slaves for my robot colony?"
    await tts_controller.speak(text)
            
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())