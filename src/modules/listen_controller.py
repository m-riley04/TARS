import sounddevice
import dotenv, json, logging, numpy as np, openwakeword as oww, pyaudio, speech_recognition as sr, vosk


class ListenController():
    """
    Controller for listening to audio input and performing actions/transcribing onto/with it.
    """
    def __init__(self, env_path: str = "../.env"):
        # Initialize logger
        self.logger = logging.getLogger('listen_controller')
        self.logger.info("Initializing ListenController...")
        
        # Initialize AssemblyAI API
        #aai.settings.api_key = dotenv.get_key(dotenv_path=env_path, key_to_get="ASSEMBLY_AI_API_KEY")
        
        # Init speech recognizer
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = False
        self.recognizer.energy_threshold = 400

        # Init microphone
        self.microphone = sr.Microphone(sample_rate=16_000, chunk_size=1280)
        
        # init offline speech recognition (vosk)
        #self.vosk_model = vosk.Model("models/vosk-model-small-en-us-0.15")
        #self.vosk_recognizer = vosk.KaldiRecognizer(self.vosk_model, 16_000)
        
        # Init wake word model
        oww.utils.download_models()
        self.wake_word_model = oww.Model(
            wakeword_models=["activation_model/hey_tars.onnx"],
            custom_verifier_models={"hey_tars": f"activation_model/training/riley_model.pkl"},
            custom_verifier_threshold=0.3,
            inference_framework="onnx")
        
        # Log
        self.logger.info("ListenController initialized successfully.")

    def listen_for_wake_phrase(self):
        """
        Continuously listens until the wake phrase(s) is detected.
        """
        self.logger.info("Waiting for wake phrase ('Hey TARS')...")
        with self.microphone as source:
            # Listen for speaking
            audio = self.recognizer.listen(source=source, phrase_time_limit=2.0)
            
            # Log
            self.logger.info("Analyzing speech...")
            
            # Transform audio to numpy array and predict wake word
            audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
            
            # Predict wake word
            predictions = self.wake_word_model.predict_clip(audio_data)
            
            # Check predictions across all segments
            detected = any(pred["hey_tars"] > 0.5 for pred in predictions)

            return detected

    def listen_for_command(self, timeout=5):
        """Listens for the command after the wake word has been detected."""
        self.logger.info("Listening for command...")
        with self.microphone as source:
            # Listen for speaking
            audio = self.recognizer.listen(source=source)
            
            transcribed_text = json.loads(self.recognizer.recognize_vosk(audio_data=audio, language="en"))["text"]
            
        
        return transcribed_text
        
        
async def main():
    # Init .env file
    import dotenv
    dotenv.load_dotenv(dotenv.find_dotenv())
    
    # Init speech controller
    listen_controller = ListenController(dotenv.find_dotenv())
    
    while True:
        print(listen_controller.listen_for_command())
   

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
