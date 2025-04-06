from google import genai
from google.genai import types
from modules.models.personality_parameters import PersonalityParameters
import dotenv, logging

AUTO_FUNCTION_CALLING = False

class ConvoController():
    """
    Controller for conversation generation using the Gemini API
    """

    def __init__(self, env_path: str = "../.env", function_declarations: list = []):
        # Initialize logger
        self.logger = logging.getLogger('convo_controller')
        self.logger.info("Initializing ConvoController...")
        
        # Initialize API 
        self.api_key = dotenv.get_key(dotenv_path=env_path, key_to_get="GEMINI_API_KEY")
        self.model = "gemini-2.0-flash"
        self.function_declarations = function_declarations
        
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
        self.memory: list[types.Content] = []
        
        # Load API clients
        self.client = genai.Client(api_key=self.api_key)
        self.tools = types.Tool(function_declarations=self.function_declarations)
        
        # Check for function declarations and set up the config accordingly
        if len(function_declarations) != 0:
            self.tools = types.Tool(function_declarations=function_declarations)
            self.config = types.GenerateContentConfig(
                tools=[self.tools],
                system_instruction=self.system_prompt,
                temperature=2.0,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=not AUTO_FUNCTION_CALLING))
        else:
            self.config = types.GenerateContentConfig(
                system_instruction=self.system_prompt,
                temperature=2.0,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=not AUTO_FUNCTION_CALLING))
        
        # Log
        self.logger.info("ConvoController initialized successfully.")
    
    def set_function_declarations(self, function_declarations: list):
        """
        Sets the function declarations for the conversation model.
        """
        self.function_declarations = function_declarations
        
        if len(function_declarations) != 0:
            self.tools = types.Tool(function_declarations=function_declarations)
            self.config = types.GenerateContentConfig(
                tools=[self.tools],
                system_instruction=self.system_prompt,
                temperature=2.0,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=not AUTO_FUNCTION_CALLING))
        else:
            self.config = types.GenerateContentConfig(
                system_instruction=self.system_prompt,
                temperature=2.0,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=not AUTO_FUNCTION_CALLING))
        
        self.logger.info("Function declarations set successfully.")
        
    def reset_memory(self):
        """
        Resets the conversation memory.
        """
        self.memory = []
        self.logger.info("Conversation memory reset.")

    def send_message(self, msg: str, personality_parameters: PersonalityParameters = None) -> tuple[str, types.FunctionCall]:
        """
        Sends a message for TARS to respond to.
        
        @returns str - The response to the sent message
        """
            
        message_text = ""
        if personality_parameters is not None:
            message_text += f"CURRENT PERSONALITY PARAMETERS: {personality_parameters}\n"
            
        message_text += f"NEW USER MESSAGE: '{msg}'"
        
        user_contents = [
            types.Content(
                role = "user",
                parts=[types.Part(text=message_text)]
            )
        ]
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=user_contents,
            config=self.config
        )
        
        # Update conversation memory with the new message and response
        self.memory.append(user_contents)
        
        ai_contents = [
            types.Content(
                role = "model",
                parts=[types.Part(text=response.text)]
            )
        ]
        
        self.memory.append(ai_contents)
        
        return (response.text, response.function_calls[0] if response.function_calls is not None else None)
    
    def send_function_result(self, function_call: types.FunctionCall, function_result: any) -> str:
        """
        Sends the result of a function call back to TARS.
        
        @returns str - The response to the sent message
        """
        
        # Create a new content object for the function result
        function_result_content = types.Part.from_function_response(
            name=function_call.name,
            response={"result": function_result},
        )
        
        # Append the function call and function result to the conversation memory
        function_call_message = types.Content(role="model", parts=[types.Part(function_call=function_call)])
        function_call_result = types.Content(role="user", parts=[function_result_content])
        
        # Generate a response based on the function result
        response = self.client.models.generate_content(
            model=self.model,
            contents=[function_call_message, function_call_result],
            config=self.config
        )
        
        # Update conversation memory with the new message and response
        self.memory.append(function_call_message)
        self.memory.append(function_call_result)
        self.memory.append(response)
        
        return response.text
        