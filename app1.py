import speech_recognition as sr
from pydub import AudioSegment
import os
INPUT_MP3_FILE = "./output.mp3"
TEMP_WAV_FILE = "temp_audio.wav"

def convert_mp3_to_wav(mp3_file, wav_file):
    try:
        audio = AudioSegment.from_mp3(mp3_file)
        audio.export(wav_file, format="wav")
        print(f"Converted {mp3_file} to {wav_file}")
        return wav_file
    except Exception as e:
        print(f"Error converting MP3 to WAV: {e}")
        return None

def speech_to_text(wav_file):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(wav_file) as source:
            print("Transcribing audio...")
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            print("Transcription completed.")
            return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Error with the Google Speech Recognition API: {e}")
        return None

def main():
    print("Starting speech-to-text conversion...")
    wav_file = convert_mp3_to_wav(INPUT_MP3_FILE, TEMP_WAV_FILE)

    if wav_file:
        transcription = speech_to_text(wav_file)
        if transcription:
            print(f"\nTranscribed Text: {transcription}")
            exported_text = transcription
            print("\nExported Text Variable Ready for Integration.")
            return exported_text

    if os.path.exists(TEMP_WAV_FILE):
        os.remove(TEMP_WAV_FILE)

if __name__ == "__main__":
    transcribed_text = main()
