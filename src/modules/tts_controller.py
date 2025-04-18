import pyttsx3 as tts
import sounddevice
import dotenv, logging
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer
from modules.models.personality_parameters import PersonalityParameters

class TtsController():
    def __init__(self, env_path: str = "../.env", offline: bool = False):
        # Initialize logger
        self.logger = logging.getLogger('tts_controller')
        self.logger.info("Initializing TTSController...")
        
        # Initialize OpenAI
        self.api_key = dotenv.get_key(dotenv_path=env_path, key_to_get="OPENAI_API_KEY")
        self.client = AsyncOpenAI(api_key=self.api_key)
        
        # Initialize offline TTS
        self.offline = offline
        self.tts_engine = tts.init() # CONSIDER: Could conditionally init based on the offline flag
        
        # Set voice properties
        self.tone = "N/A"
        self.voice_affect = "N/A"
        self.pacing = "Slightly faster than average human speech."
        self.emotion = "N/A"
        self.pronunciation = "Articulate, minimal variation."
        self.pauses = "VERY, VERY brief pauses strategically placed after humorous or sarcastic remarks for deadpan comedic effect."
        
        # Log
        self.logger.info("TTSController initialized successfully.")

    async def speak(self, text, personality_parameters: PersonalityParameters = None):
        """Speaks the given text using TTS."""
        if self.offline:
            # Use offline TTS engine
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            return
        
        _instructions = f"""Voice Affect: {self.voice_affect}
            Tone: {self.tone}
            Pacing: {self.pacing}
            Emotion: {self.emotion}
            Pronunciation: {self.pronunciation}
            Pauses: {self.pauses}"""
        
        if personality_parameters is not None:
            _instructions += f"\nPersonality Parameters:\n{personality_parameters}"
        
        async with self.client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",#"tts-1",
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
