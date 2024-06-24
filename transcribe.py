import time
import sys
import subprocess
import os
import speech_recognition as sr

# Ensure pydub is installed
try:
    from pydub import AudioSegment
    print("pydub imported successfully")
except ModuleNotFoundError:
    print("pydub not found, installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pydub"])
    from pydub import AudioSegment
    print("pydub installed and imported successfully")

# Convert .m4a to .wav
audio_file = "voice.m4a"  # Replace with your audio file path
wav_file = "voice.wav"
text_file = "transcription.txt"  # Output text file

# Check if audio file exists
if not os.path.exists(audio_file):
    print(f"Audio file {audio_file} does not exist")
    sys.exit(1)

# Load your .m4a file
print("Loading audio file...")
audio = AudioSegment.from_file(audio_file, format="m4a")
print("Audio file loaded")

# Export as .wav
print("Converting audio file to .wav format...")
audio.export(wav_file, format="wav")
print("Audio file converted to .wav format")

# Initialize recognizer
recognizer = sr.Recognizer()

# Load converted audio file
print("Loading converted audio file...")
with sr.AudioFile(wav_file) as source:
    audio_data = recognizer.record(source)
print("Converted audio file loaded")

# Retry mechanism for transcribing audio file
def transcribe_audio(audio_data, attempts=3):
    for attempt in range(attempts):
        try:
            print("Transcribing audio file (attempt {}/{})...".format(attempt + 1, attempts))
            text = recognizer.recognize_google(audio_data)
            print("Transcription successful")
            return text
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            if attempt < attempts - 1:
                print("Retrying...")
                time.sleep(5)  # Wait for 5 seconds before retrying
            else:
                print("All attempts failed.")
                raise
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return None

# Transcribe audio and save to file
try:
    text = transcribe_audio(audio_data)
    if text:
        print("Text: " + text)
        # Save the text to a file
        with open(text_file, "w") as file:
            file.write(text)
        print(f"Transcription saved to {text_file}")
except Exception as e:
    print(f"Transcription failed: {e}")

# Optional: Remove the converted .wav file if no longer needed
os.remove(wav_file)
print("Temporary .wav file removed")
