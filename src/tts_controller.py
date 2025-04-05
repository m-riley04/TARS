import pyttsx3 as tts
import dotenv
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer
from personality_parameters import PersonalityParameters

class TtsController():
    def __init__(self, env_path: str = "../.env"):
        self.api_key = dotenv.get_key(dotenv_path=env_path, key_to_get="OPENAI_API_KEY")
        self.tts_engine = tts.init()
        self.client = AsyncOpenAI(api_key=self.api_key)
        
        # Set voice properties
        self.tone = "Matter-of-fact, understated wit, professionally detached."
        self.voice_affect = "Neutral, dry, calmly authoritative, slightly mechanical."
        self.pacing = "Steady, deliberate, slightly faster than average human speech."
        self.emotion = "Controlled neutrality with occasional subtle amusement."
        self.pronunciation = "Crisp, articulate, mildly robotic with minimal variation."
        self.pauses = "Brief pauses strategically placed after humorous or sarcastic remarks for deadpan comedic effect."

    async def speak(self, text):
        async with self.client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="onyx",
            input=text,
            instructions=f"""Voice Affect: {self.voice_affect}
            Tone: {self.tone}
            Pacing: {self.pacing}
            Emotion: {self.emotion}
            Pronunciation: {self.pronunciation}
            Pauses: {self.pauses}"""
        
        if personality_parameters is not None:
            _instructions += f"\nPersonality Parameters:\n{personality_parameters}"
        
        async with self.client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="onyx",
            input=text,
            instructions=_instructions,
            response_format="pcm"
        ) as response:
            await LocalAudioPlayer().play(response)

async def main():
    # Init .env file
    import dotenv
    dotenv.load_dotenv(dotenv.find_dotenv())
    
    tts_controller = TtsController()
    text = "Hey there, I'm TARS."
    await tts_controller.speak(text)
            
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())