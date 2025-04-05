# TARS
A real-life version of the robot TARS from the motion picture *Interstellar*; created as a HackKU hackathon project.
- Project Devpost Page <!-- Add link here -->
- HackKU 2025 Devpost <!-- Add link here -->
- HackKU Website <!-- Add link here -->

# Software Components
The major components of TARS' software can be found below.
## Top-Level Controller
At the top-most level, we have the main controller. This is responsible for managing all the other controllers and holding the main runtime loop. It also is the source of truth for TARS' personality parameters.

## Wake Word Model
We used the `openwakeword` [Python package](https://github.com/dscripka/openWakeWord) and [trained](https://github.com/dscripka/openWakeWord?tab=readme-ov-file#training-new-models) our own custom ONNX model to "wake" TARS from an idle state to be actively listening for commands.

We also trained verifier models to further improve the performance and accuracy of the wake phrase's activation, allowing us to select exactly who TARS responds to.

## Speech-to-Text Controller
We utilized AssemblyAI to transcribe the user's commands/questions to TARS, that were then passed on to the Google Gemini model.
<!-- Add stuff here -->

## Conversational Controller
We utilized Google Gemini API for TARS' conversationalism and action control. We went with the 
<!-- Add stuff here -->

## Text-to-Speech Controller
We utilized [OpenAI's text-to-speech API](https://platform.openai.com/docs/guides/text-to-speech) to give TARS a voice. The exact model we used was `gpt-4o-mini-tts`, with the `onyx` voice.

We also utilized the `pyttsx3` package for the off-chance that we are unable to access OpenAI's model due to being offline.

## Servo Controller
<!-- Add stuff here -->

# Hardware Components
The major components of TARS' hardware can be found below.
## Microcomputer
<!-- Add stuff here -->
## Servos
<!-- Add stuff here -->
## Screen
<!-- Add stuff here -->
## Battery
<!-- Add stuff here -->
## Speaker and Amplifier
<!-- Add stuff here -->
## Microphone
<!-- Add stuff here -->
## 3D Prints
<!-- Add stuff here -->

# Info
- Python 3.10.11
- PiOS <!-- Add version here -->
<!-- Add more stuff here -->

# Dependencies
Dependencies can be found within the [requirements](REQUIREMENTS.txt) file, and can be batch installed with the following `pip` command:

```bash
pip install -r REQUIREMENTS.txt
```