import openwakeword
import os
from pydub import AudioSegment 

PERSON = "riley"

def absoluteFilePaths(directory):
    """
    Gets a list of absolute file paths for all files in a directory
    """
    _ = []
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            _.append(os.path.abspath(os.path.join(dirpath, f)))
            
    return _

def convert_to_16k_mono(input_path, output_path):
    audio: AudioSegment = AudioSegment.from_file(input_path)
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    audio.export(output_path, format="wav")

def convert_directory(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.wav', '.mp3', '.ogg')):
            convert_to_16k_mono(
                os.path.join(input_dir, filename),
                os.path.join(output_dir, filename.replace(".mp3", ".wav").replace(".ogg", ".wav"))
            )

def main():
    # Check if person directory exists
    if not os.path.exists(f"{os.getcwd()}/models/training/{PERSON}"):
        print(f"ERROR: '{PERSON}' directory does not exist")
        return
    
    # Check if positive reference clips folder exists
    if not os.path.exists(f"{os.getcwd()}/models/training/{PERSON}/positive"):
        print("ERROR: positive reference clips directory does not exist")
        return
    
    # Check if negative reference clips folder exists
    if not os.path.exists(f"{os.getcwd()}/models/training/{PERSON}/negative"):
        print("ERROR: negative reference clips directory does not exist")
        return
    
    # Convert the audio files to the correct format
    base_dir = os.path.join(os.getcwd(), "models", "training", PERSON)

    convert_directory(f"{os.getcwd()}/models/training/{PERSON}/positive", f"{os.getcwd()}/models/training/{PERSON}/positive")
    convert_directory(f"{os.getcwd()}/models/training/{PERSON}/negative", f"{os.getcwd()}/models/training/{PERSON}/negative")
    
    # Get positive and negative reference clips
    pos = absoluteFilePaths(f"{os.getcwd()}/models/training/{PERSON}/positive")
    neg = absoluteFilePaths(f"{os.getcwd()}/models/training/{PERSON}/negative")
    
    # Train the custom verifier
    openwakeword.train_custom_verifier(
        positive_reference_clips = pos,
        negative_reference_clips = neg,
        output_path = f"{os.getcwd()}/models/training/{PERSON}_model.pkl",
        model_name = f"{os.getcwd()}\\models\\hey_tars.onnx"
    )

if __name__ == "__main__":
    main()