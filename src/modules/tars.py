from modules.listen_controller import ListenController
from modules.convo_controller import ConvoController
from modules.tts_controller import TtsController
from modules.models.personality_parameters import PersonalityParameters
import logging

class TARS:
    def __init__(self, env_path: str = "../.env"):
        # Configure logging
        self.logger = logging.getLogger('tars')
        self.logger.info("Initializing TARS...")
        
        # Initailize controllers
        self.listen_controller = ListenController(env_path=env_path)
        self.convo_controller = ConvoController(env_path=env_path)
        self.tts_controller = TtsController(env_path=env_path)
        self.personality_parameters = PersonalityParameters()
        
        # Log the initialization
        self.logger.info("TARS initialized successfully.")
    
    async def run(self):
        """Runs the program"""
        self.logger.info("Beginning main runtime loop...")
        
        # Main runtime loop
        while True:
            # Wait for the wake phrase
            detected = self.listen_controller.listen_for_wake_phrase()
            
            # Check if the transcript contains wake word(s)/phrase(s)
            if detected:
                self.logger.info("Wake phrase detected!")
            else:
                self.logger.warning("Wake phrase not detected. Please try again.")
                continue

            # Listen for the command after the wake word has been detected
            user_command = self.listen_controller.listen_for_command()
            
            # Check command validity
            if user_command is None:
                self.logger.warning("No command detected. Please try again.")
                continue
            
            # Generate a repsonse using Gemini
            response = self.convo_controller.send_message(
                msg={user_command},
                personality_parameters=self.personality_parameters
            )
            
            # Print the response
            self.logger.info("=== REPLY FROM TARS ===")
            self.logger.info(f'"{response}"')
            self.logger.info("=== END OF MESSAGE ===")
            
            # Speak the response using TTS
            await self.tts_controller.speak(response, self.personality_parameters)
            