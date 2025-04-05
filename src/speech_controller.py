import speech_recognition as sr
import assemblyai as aai
import dotenv
import openwakeword
import numpy as np
import os

class SpeechController():
    def __init__(self, env_path: str = "../.env"):
        aai.settings.api_key = dotenv.get_key(dotenv_path=env_path, key_to_get="ASSEMBLY_AI_API_KEY")
        
        # Init speech recognizer
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = False
        self.recognizer.energy_threshold = 500

        # Init microphone
        self.microphone = sr.Microphone(sample_rate=16000, chunk_size=1280)
        
        # Init transcriber (text to speech)
        self.transcriber = aai.Transcriber()
        
        # Init wake word model
        openwakeword.utils.download_models()
        self.wake_word_model = openwakeword.Model(
            wakeword_models=["models/hey_tars.onnx"],
            custom_verifier_models={"hey_tars": f"models/training/riley_model.pkl"},
            custom_verifier_threshold=0.3,
            inference_framework="onnx")

    def listen_for_wake_phrase(self):
        """
        Continuously listens until the wake phrase(s) is detected.
        """
        print("Waiting for wake phrase ('Hey TARS')...")
        with self.microphone as source:
            # Listen for speaking
            audio = self.recognizer.listen(source=source, phrase_time_limit=1.5)
            
            # Notify user
            print("Predicting wake word...")
            
            audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
            predictions = self.wake_word_model.predict_clip(audio_data)
            
            #print("Predictions:", predictions)
            
            # Check predictions across all segments
            detected = any(pred["hey_tars"] > 0.5 for pred in predictions)

            return detected

    def listen_for_command(self):
        """Listens for the command after the wake word has been detected."""
        print("Listening for command...")
        with self.microphone as source:
            audio = self.recognizer.listen(source)
            
            command = self.transcriber.transcribe_async(audio.get_wav_data()) #self.recognizer.recognize_assemblyai(audio.get_wav_data(), api_token=self.assembly_ai_api_key)
            
            # Notify user
            print("Transcribing command...")
            
            # Wait for transcription to complete
            while command.running():
                # Check if the transcription is complete
                if command.done():
                    break
                
            # Check for errors or cancellation
            if command.exception():
                print("Transcription error:", command.exception())
                return
            elif command.cancelled():
                print("Transcription cancelled")
                return
            
            _result = command.result()
                
            # Print the recognized command
            print(f"Transcribed command: {_result.text}\nConfidence: {_result.confidence}")
            return _result.text
        
        
async def main():
    # Init .env file
    import dotenv
    dotenv.load_dotenv(dotenv.find_dotenv())
    
    # Init speech controller
    speech_controller = SpeechController(dotenv.find_dotenv())
    
    while True:
        speech_controller.listen_for_wake_phrase()
   

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())