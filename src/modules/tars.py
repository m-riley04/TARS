from modules.listen_controller import ListenController
from modules.convo_controller import ConvoController
from modules.tts_controller import TtsController
from modules.models.personality_parameters import PersonalityParameters
import logging, threading, queue
from google.genai import types
from modules.tars_tools import TarsTools
import sounddevice
from modules.servo_controller import walk, run_declaration 

from modules.text_controller import run_gui


update_personality_declaration = {
    "name": "update_personality",
    "description": "Update or set a personality parameter for TARS.",
    "parameters": {
        "type": "object",
        "properties": {
            "parameter": {
                "type": "string",
                "description": "The personality parameter to update (e.g., 'humor', 'sarcasm')."
            },
            "value": {
                "type": "number",
                "description": "The new value for the personality parameter (expected to be between 0.0 and 1.0)."
            }
        },
        "required": ["parameter", "value"]
    }
}

get_weather_declaration = {
    "name": "get_weather",
    "description": "Get the current weather information for a given location. Returns dummy weather data.",
    "parameters": {
        "type": "object"
    }
}

walk_declaration = {
    "name": "walk",
    "description": "Walk in a particular direction.",
    "parameters": {
        "type": "object",
        "properties": {
            "direction": {
                "type": "string",
                "description": "The direction to walk in.",
                "enum": ["forward", "backward"]
            },
            "steps": {
                "type": "number",
                "description": "The amount of steps."
            }
        },
        "required": ["direction", "steps"]
    }
}

run_dec = {
    "name": "run_dec",
    "description": "Run a particular distance.",
    "parameters": {
        "type": "object",
        "properties": {
            "direction": {
                "type": "string",
                "description": "The direction to run in.",
                "enum": ["forward", "backward"]
            },
            "distance": {
                "type": "number",
                "description": "The distance in centimeters."
            }
        },
        "required": ["direction", "distance"]
    }
}

shutdown = {
    "name": "shutdown",
    "description": "Terminates the program.",
    "parameters": {
        "type": "object",
    }
}

diagnostics = {
    "name": "diagnostics",
    "description": "Performs a diagnostics check on the system.",
    "parameters": {
        "type": "object"
    }
}

wave = {
    "name": "wave",
    "description": "Waves at the user.",
    "parameters": {
        "type": "object",
    }
}

clear_conversation = {
    "name": "clear_conversaion",
    "description": "Clears the conversation history.",
    "parameters": {
        "type": "object"
    }
}

class TARS:
    def __init__(self, env_path: str = "../.env"):
        # Configure logging
        self.logger = logging.getLogger('tars')
        self.logger.info("Initializing TARS...")
        
        # Queueing and gui
        self.gui_queue = queue.Queue()
        
        # Initialize personality
        self.personality_parameters = PersonalityParameters()
        
        # Initailize controllers
        self.listen_controller = ListenController(env_path=env_path)
        self.convo_controller = ConvoController(env_path=env_path, function_declarations=[
            update_personality_declaration, 
            get_weather_declaration, 
            diagnostics, 
            wave, 
            shutdown,
            run_dec,
            clear_conversation])
        self.tts_controller = TtsController(env_path=env_path)
        
        # Log the initialization
        self.logger.info("TARS initialized successfully.")
        
    def action_update_personality(self, parameter: str, value: float):
        """Updates the personality parameter for TARS"""
        try:
            # Update the personality parameter
            self.personality_parameters.update(parameter, value)
            self.logger.info(f"Personality parameter '{parameter}' updated to {value}.")
        except ValueError as e:
            self.logger.error(e)
            
    def action_shutdown(self):
        """Shuts down the program"""
        # self.logger.info("Shutting down TARS...")
        # sounddevice.stop()
        # sounddevice.close()
        # exit(0)
        pass
    
    def action_diagnostics(self):
        """Moves both arms up and down to check the motors"""
        # TODO: implement the diagnostics check action
        return "Diagnostics check complete."
    
    def action_wave(self):
        """Moves the arm to wave at the user"""
        # TODO: implement the wave action
        return "Waving at the user."
    
    def action_clear_conversaion(self):
        """Clears the conversaion history"""
        
        self.convo_controller.reset_memory()
        self.gui_queue.put({"clear": True})
        
        return "Conversation history cleared."
    
    def action_run(self):
        """Runs the bot"""
        
        run_declaration(self, 5, "forward")
        
        return "Running successful."
    
    def action_walk(self):
        """Walks the bot"""
        
        walk(self, 5, "forward")
        
        return "Walking successful."
        
    def perform_function_call(self, function_call: types.FunctionCall):
        """Performs the function call using the TARS tools"""
        self.logger.info(f"Performing function call: {function_call.name} with arguments: {function_call.args}")
        
        args = function_call.args  # This should be a dictionary
        
        if function_call.name == "update_personality":
            parameter = args.get("parameter")
            value = args.get("value")
            self.action_update_personality(parameter, value)
                
        if function_call.name == "get_weather": 
            weather_info = TarsTools.get_weather()
            
            # Log the weather information
            self.logger.info(f"Weather information: {weather_info}")
            
            return weather_info
        
        if function_call.name == "diagnostics": 
            ret = self.action_diagnostics()
            
            # Log
            self.logger.info(f"Diagnostics: {ret}")
            
            return ret
        
        if function_call.name == "shutdown": 
            ret = self.action_shutdown()
            
            # Log
            self.logger.info(f"Shutting down: {ret}")
            
            return ret
        
        if function_call.name == "wave": 
            ret = self.action_wave()
            
            # Log
            self.logger.info(f"Waving: {ret}")
            
            return ret
        
        if function_call.name == "clear_conversation": 
            ret = self.action_clear_conversaion()
            
            # Log
            self.logger.info(f"Cleared conversation: {ret}")
            
            return ret
            
    
    async def run(self):
        """Runs the program"""
        self.logger.info("Beginning main runtime loop...")
        
        gui_thread = threading.Thread(target=run_gui, args=(self.gui_queue,), daemon=True)
        gui_thread.start()
        
        await self.tts_controller.speak("I am now online.", self.personality_parameters)
        while True:
            
            # Wait for the wake phrase
            detected = self.listen_controller.listen_for_wake_phrase()
            
            # Check if the transcript contains wake word(s)/phrase(s)
            if not detected:
                self.logger.warning("Wake phrase not detected. Please try again.")
                continue
            
            self.logger.info("Wake phrase detected!")
            print('\a')  # Beep sound
                
            # TODO: Lean forward and listen for the command
            
            # Before listening for the command, update the GUI to show the listening indicator.
            self.gui_queue.put({"listening": True})

            # Listen for the command after the wake word has been detected
            user_command = self.listen_controller.listen_for_command()
            
            # Send GUI update again
            self.gui_queue.put({"listening": False})
            # TODO: Lean backward and stop listening
            
            # Check command validity
            if user_command is None:
                self.logger.warning("No command detected. Please try again.")
                continue
            
            # Generate a repsonse using Gemini
            response = self.convo_controller.send_message(
                msg={user_command},
                personality_parameters=self.personality_parameters
            )
            
            response_text = response[0]
            response_function_call = response[1]
            
            if response_function_call is not None:
                # Perform the function call if it exists
                self.logger.info(f"Function call detected: {response_function_call.name}")
                result = self.perform_function_call(response_function_call)
                if result is not None:
                    response = self.convo_controller.send_function_result(response_function_call, result)
                    response_text = response
            
            # Print the response
            self.logger.info("=== REPLY FROM TARS ===")
            self.logger.info(f'"{response_text}"')
            self.logger.info("=== END OF MESSAGE ===")
            
            # Send the response text to the GUI (thread-safe)
            self.gui_queue.put(response_text)
            
            # Speak the response using TTS
            await self.tts_controller.speak(response_text, self.personality_parameters)
            
