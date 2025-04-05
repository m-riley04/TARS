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

    def listen_for_wake_word(self):
        """Continuously listens until the wake word is detected."""
        print("Waiting for wake word ('Hey TARS' or 'TARS')...")
        while True:
            with self.microphone as source:
                audio = self.recognizer.listen(source)
            try:
                transcript = self.transcriber.transcribe(audio.get_wav_data()) #self.recognizer.recognize_assemblyai(audio.get_wav_data(), api_token=self.assembly_ai_api_key)
                print("Heard:", transcript.text)
                # Check if the transcript contains wake word(s)/phrase(s)
                if "tars" in transcript.text.lower():
                    print("Wake word detected")
                    break
            except sr.UnknownValueError:
                # Speech was unintelligible, continue listening
                continue
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                continue

    def listen_for_command(self):
        """Listens for the command after the wake word has been detected."""
        print("Listening for command...")
        with self.microphone as source:
            audio = self.recognizer.listen(source)
        try:
            command = self.transcriber.transcribe(audio.get_wav_data()) #self.recognizer.recognize_assemblyai(audio.get_wav_data(), api_token=self.assembly_ai_api_key)
            print(f"Command recognized: {command.text}\nConfidence: {command.confidence}")
            return command.text
        except sr.UnknownValueError:
            print("AssemblyAI Speech Recognition could not understand the audio")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return ""