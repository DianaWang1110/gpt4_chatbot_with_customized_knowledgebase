"""Module to generate transcript from local downloaded file"""
import whisper
import ffmpeg

from audio_video_summary.constants import *


# Generate transcript from the text given the filepath, desired speech to text service (eg google or whisper) and model
# For whisper, tiny or base is recommended, as performance is good enough and larger models take way too long
def audio_to_text(filepath, service, model):
    print("not yet implemented")


# When using this function, make sure to check if output is None
def mp3_to_text_whisper(filepath, model="tiny"):
    if model.lower() not in ALLOWED_WHISPER_MODELS:
        print("Model is not a correct whisper model")
        return None
    if model.lower() == "medium" or model.lower() == "large":
        print("WARNING: Medium and large models may take hours to transcribe audio")
    try:
        model = whisper.load_model(model)
        result = model.transcribe(filepath)
        return result["text"]
    except Exception as e:
        print("Error in loading model or transcribing in mp3_to_text_whisper:")
        print(e)
        return None
