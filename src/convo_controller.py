from google import genai
import dotenv

class ConvoController():
    """Controller for conversation generation using the Gemini API"""

    def __init__(self, env_path: str = "../.env"):
        self.api_key = dotenv.get_key(dotenv_path=env_path, key_to_get="GEMINI_API_KEY")
        self.model = "gemini-2.0-flash"
        self.system_prompt = "You are TARS, a robot from the movie Interstellar. You are very helpful and witty."
        
        # Load API clients
        self.client = genai.Client(api_key=self.api_key)

    def send_message(self, user_command: str) -> str:
        """Generate a response using the Gemini API"""
        response = self.client.models.generate_content(
            model=self.model,
            contents=f"{self.system_prompt}\nThe user said: '{user_command}'."
        )
        return response.text