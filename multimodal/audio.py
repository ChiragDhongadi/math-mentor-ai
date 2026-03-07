import sys
import os
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from faster_whisper import WhisperModel
from utils.math_speech_cleaner import clean_math_speech

# Force CPU mode
model = WhisperModel("base", device="cpu", compute_type="int8")


def transcribe_audio(audio_file):

    segments, _ = model.transcribe(audio_file)

    text = ""
    scores = []

    for segment in segments:
        text += segment.text
        # Convert log probability to linear probability
        scores.append(math.exp(segment.avg_logprob))

    # Calculate average confidence
    avg_confidence = sum(scores) / len(scores) if scores else 0.0

    cleaned = clean_math_speech(text)

    return cleaned, avg_confidence

# TEST
if __name__ == "__main__":

    audio_path = "sumit_tts_audio.mp3"

    text, conf = transcribe_audio(audio_path)

    print(f"\nTranscription ({conf:.2f}):\n")
    print(text)
