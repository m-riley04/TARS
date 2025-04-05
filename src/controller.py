from speech_controller import SpeechController
from convo_controller import ConvoController

class Controller:
    def __init__(self, env_path: str = "../.env"):
        self.speech_controller = SpeechController(env_path=env_path)
        self.convo_controller = ConvoController(env_path=env_path)
        
        # Load API clients
        self.client = genai.Client(api_key=self.gemini_api_key)
    
    def run(self):
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
            
        self.speech_controller.listen_for_wake_word()
        
        user_command = ""
        while user_command == "":
            # Listen for the command after the wake word has been detected
            user_command = self.speech_controller.listen_for_command()
        
        # Generate a repsonse using Gemini
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"You are TARS, a robot from the movie Interstellar. You are very helpful and witty. The user said: '{user_command}'. Please provide a witty response or tell a joke.",
        )
        
        print(response.text)