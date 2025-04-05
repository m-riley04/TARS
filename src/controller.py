from speech_controller import SpeechController
from convo_controller import ConvoController
from tts_controller import TtsController
from personality_parameters import PersonalityParameters

class Controller:
    def __init__(self, env_path: str = "../.env"):
        self.speech_controller = SpeechController(env_path=env_path)
        self.convo_controller = ConvoController(env_path=env_path)
        self.tts_controller = TtsController(env_path=env_path)
        self.personality_parameters = PersonalityParameters()
    
    async def run(self):
        """Runs the program"""
        
        # Main runtime loop
        while True:
            # Wait for the wake phrase
            phrase = self.speech_controller.listen_for_wake_phrase()
            
            # Check if the transcript contains wake word(s)/phrase(s)
            if "hey tars" in phrase.lower() or "hey, tars" in phrase.lower():
                print("Wake phrase detected!")
            else:
                print("Wake phrase not detected. Please try again.")
                continue

            # Listen for the command after the wake word has been detected
            user_command = self.speech_controller.listen_for_command()
            
            # Check command validity
            if user_command is None:
                print("No command detected. Please try again.")
                continue
            
            # Generate a repsonse using Gemini
            response = self.convo_controller.send_message(
                msg={user_command},
                personality_parameters=self.personality_parameters
            )
            
            # Print the response
            print("=== REPLY FROM TARS ===")
            print(f'"{response}"')
            print("=== END OF MESSAGE ===")
            
            # Speak the response using TTS
            await self.tts_controller.speak(response, self.personality_parameters)
            
            