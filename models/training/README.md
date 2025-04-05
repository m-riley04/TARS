# Training Verifier Models
To train verifiers, I followed the procedure given by the [openWakeWord library](https://github.com/dscripka/openWakeWord/blob/main/docs/custom_verifier_models.md). I have attempted to simplify it further.

To train a verifier model, follow these steps:
1. Create a new folder with your name in this directory
2. Inside that subfolder, create 2 folders:
  - negative
  - positive
3. Using an audio recording software of your choice (preferrably Audacity), record the required positive and negative audio clips as detailed in the [openWakeWord custom verifier README](https://github.com/dscripka/openWakeWord/blob/main/docs/custom_verifier_models.md).
  - Positive clips should be the wake phrase ("Hey Tars"), and you should try to have some variation between them (but keep them within ~1.5 seconds)
  - Negative clips should NOT be the wake phrase, but other phrases and sentences (examples: "The quick brown fox jumped over the lazy dog")
  - Do not use too many negative clips. Keep it to a maximum of 10-15 seconds.
4. Using the `train_verifier.py` script, replace the `NAME` constant with your own
5. Run the `train_verifier.py` script, and the verifier model will be generated in this directory in the format `[your_name]_model.pkl`