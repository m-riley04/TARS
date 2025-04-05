import openwakeword
import os

PERSON = "riley"

def main():
    # Check if person directory exists
    if not os.path.exists(PERSON):
        print("ERROR: person directory does not exist")
        return
    
    # Check if positive reference clips folder exists
    if not os.path.exists(f"{PERSON}/positive"):
        print("ERROR: positive reference clips folder does not exist")
        return
    
    # Check if negative reference clips folder exists
    if not os.path.exists(f"{PERSON}/negative"):
        print("ERROR: negative reference clips folder does not exist")
        return
    
    # Get positive and negative reference clips
    pos = os.listdir(f"{PERSON}/positive")
    neg = os.listdir(f"{PERSON}/negative")
    
    print(pos)
    
    print(neg)
    
    # Train the custom verifier
    # openwakeword.train_custom_verifier(
    #     positive_reference_clips = pos,
    #    negative_reference_clips = neg,
    #     output_path = f"../{PERSON}_model.pk1",
    #     model_name = "../hey_tars.onnx",
    # )

if __name__ == "__main__":
    main()