import dotenv
from google import genai
from speech_controller import SpeechController

class Controller:
    def __init__(self, env_path: str = "../.env"):
        # Load environment variables
        self.gemini_api_key = dotenv.get_key(dotenv_path=env_path, key_to_get="GEMINI_API_KEY")
        self.speech_controller = SpeechController(env_path=env_path)
        
        # Load API clients
        self.client = genai.Client(api_key=self.gemini_api_key)
    
    def run(self):
        """Runs the program"""
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