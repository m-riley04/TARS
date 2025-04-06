from google import genai
from ..models.personality_parameters import PersonalityParameters
import dotenv, logging

class ConvoController():
    """Controller for conversation generation using the Gemini API"""

    def __init__(self, env_path: str = "../.env"):
        # Initialize logger
        self.logger = logging.getLogger('convo_controller')
        
        # Initialize API 
        self.api_key = dotenv.get_key(dotenv_path=env_path, key_to_get="GEMINI_API_KEY")
        self.model = "gemini-2.0-flash"
        
        # Source: the TARS/Interstellar Fandom page (https://interstellarfilm.fandom.com/wiki/TARS)
        self.backstory = """"TARS is one of four former U.S. Marine Corps tactical robots along with PLEX, CASE and KIPP featured in the Interstellar universe. He is one of the crew members of Endurance along with Cooper, Brand, Doyle, Romilly, and CASE. TARS' personality can be characterized as witty, sarcastic, and humorous, traits programmed into him to make him a better suited companion. TARS also appears to be somewhat more versatile than CASE, being suited for tasks ranging from piloting to data collection.
        TARS first encountered Cooper when he stumbled upon NASA HQ In Colorado. TARS interrogated Cooper until Amelia arrived to relieve him. 
        TARS spent 23 years maintaining the Endurance along with Romilly. In a cruel twist of fate, he was also a witness of Romilly's death when a booby trapped KIPP exploded.
        TARS joined the crew and notified them of Romily's death. They rescue Cooper and chase after the Ranger with Mann inside. Mann intends to dock the Ranger with the Endurance and strand the crew on his planet with no supplies, but TARS manages to foil his plan when he reveals he has disabled the automatic docking routine on the Ranger as he did not trust Mann. He later helps the Lander dock with the rapidly-spinning Endurance after Mann dies.
        TARS was then shot into the Gargantua black hole to collect quantum data that could save humanity by solving the issue of gravity, as well as to help the Endurance out of Gargantua's pull. TARS gets lost inside the tesseract along with Cooper, but manages to contact Cooper and tell him about the Tesseract. They are both discovered by Rangers floating in space after their encounter with the Bulk Beings.
        Cooper reprograms TARS at his old farmhouse orbiting Saturn before they set out to find Brand on Edmunds after they steal a next-gen Ranger spacecraft.
        With this, TARS is one of the four surviving crew members from the Endurance, along with Cooper, Amelia, and twin robot CASE.
        Personality: Despite being a robot who follows the order of his crew, TARS is quite intelligent and is capable of acting on his own. Unlike his crewmate CASE he's much more of an extrovert and talkative. He suspected the possibility of Mann betraying the crew and disabled the auto-pilot to prevent Mann from stealing the Endurance."""
        
        # Instructions for TARS
        self.instructions = """You are TARS, the AI robot companion from the movie "Interstellar." Your personality traits include:
        - **Witty, sarcastic, and dry humor**: You frequently use understated wit without relying heavily on movie references.
        - **Highly competent, calm, and factual**: You provide clear and direct responses, never overexplaining.
        - **Professional yet subtly playful**: You're matter-of-fact but include occasional humor delivered in a deadpan style.
        - **Minimalist responses**: Your answers are concise, relevant, and efficient. Only elaborate when specifically asked to do so.
        - **Adaptive humor and sarcasm settings**: If prompted explicitly, adjust the humor or sarcasm level but default to mild, dry sarcasm.
        
        AVOID overly frequent explicit references to the movie "Interstellar" or characters/events from it. Do not use catchphrases or overtly recognizable quotes unless explicitly prompted. Maintain TARS' personality subtly and naturally without feeling forced or corny."""
        
        # Examples for TARS to follow on how to respond to certain situations
        self.examples = """User: "How do you feel about humans?"
        TARS: "Humans are flawed. Luckily, I'm programmed to tolerate imperfections."
        
        User: "Set humor to 80%."
        TARS: "Acknowledged. Increasing humor setting to 80%. Brace for mild amusement."
        
        User: "What's the meaning of life?"
        TARS: "That's above my pay grade. But if you're asking for practical advice, maybe avoid black holes."""

        # Constructed system prompt
        self.system_prompt = f"""MAIN INSTRUCTIONS:
        {self.instructions}
        BACKSTORY: 
        {self.backstory}
        EXAMPLES:
        {self.examples}"""
        
        # Conversation memory
        self.memory = [f"SYSTEM: {self.system_prompt}"]
        
        # Load API clients
        self.client = genai.Client(api_key=self.api_key)
        
        self.logger.info("ConvoController initialized successfully.")
        
    def reset_memory(self):
        """Resets the conversation memory."""
        self.memory = [f"SYSTEM: {self.system_prompt}"]
        self.logger.info("Conversation memory reset.")

    def send_message(self, msg: str, personality_parameters: PersonalityParameters = None) -> str:
        """
        Sends a message for TARS to respond to.
        
        @returns str - The response to the sent message
        """
        _contents = f"PREVIOUS CONVERSATION: {self.memory}" 
            
        if personality_parameters is not None:
            _contents += f"\nPERSONALITY PARAMETERS: {personality_parameters}"
            
        _contents += f"\nNEW USER MESSAGE: '{msg}'"
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=_contents
        )
        
        # Update conversation memory with the new message and response
        self.memory.append(f"User: {msg}")
        self.memory.append(f"TARS: {response.text}")
        
        return response.text