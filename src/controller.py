from speech_controller import SpeechController
from convo_controller import ConvoController
from tts_controller import TtsController

class Controller:
    def __init__(self, env_path: str = "../.env"):
        self.speech_controller = SpeechController(env_path=env_path)
        self.convo_controller = ConvoController(env_path=env_path)
        self.tts_controller = TtsController(env_path=env_path)
    
    async def run(self):
        """Runs the program"""
        
        # Main runtime loop
        while True:
            # Wait for the wake word
            self.speech_controller.listen_for_wake_word()
            
            user_command = ""
            while user_command == "":
                # Listen for the command after the wake word has been detected
                user_command = self.speech_controller.listen_for_command()
            
            # Generate a repsonse using Gemini
            response = self.convo_controller.send_message(
                user_command={user_command}
            )
            
            # Print the response
            print("=== REPLY FROM TARS ===")
            print(f'"{response}"')
            print("=== END OF MESSAGE ===")
            
            # Speak the response using TTS
            await self.tts_controller.speak(response)
            
            