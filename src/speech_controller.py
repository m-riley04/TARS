import speech_recognition as sr
import assemblyai as aai
import dotenv

class SpeechController():
    def __init__(self, env_path: str = "../.env"):
        aai.settings.api_key = dotenv.get_key(dotenv_path=env_path, key_to_get="ASSEMBLY_AI_API_KEY")
        
        # Init speech recognizer and microphone
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Init transcriber (text to speech)
        self.transcriber = aai.Transcriber()

    def listen_for_wake_phrase(self):
        """Continuously listens until the wake phrase(s) is detected."""
        print("Waiting for wake phrase ('Hey TARS')...")
        with self.microphone as source:
            # Listen for speaking
            audio = self.recognizer.listen(source)
            
            # Transcribe audio
            transcript = self.transcriber.transcribe_async(audio.get_wav_data()) #self.recognizer.recognize_assemblyai(audio.get_wav_data(), api_token=self.assembly_ai_api_key)
            
            # Notify user
            print("Transcribing wake phrase...")
            
            # Wait for transcription to complete
            while transcript.running():
                # Check if the transcription is complete
                if transcript.done():
                    break
                
            # Check for errors or cancellation
            if transcript.exception():
                print("Transcription error:", transcript.exception())
                return
            elif transcript.cancelled():
                print("Transcription cancelled")
                return
            
            _result = transcript.result()
            
            # Print what was heard
            print("Heard:", _result.text)
            
            return _result.text

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