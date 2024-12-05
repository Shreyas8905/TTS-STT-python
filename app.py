import os
import wave
from gtts import gTTS
import pyaudio

TEXT_TO_SPEECH = "Hello, I am from Bengaluru"
LANGUAGE = "en"
OUTPUT_FILE = "output.mp3"

def text_to_speech(text, lang, output_file):
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(output_file)
        print(f"Audio saved to {output_file}")
        return output_file
    except Exception as e:
        print(f"An error occurred while generating speech: {e}")
        return None

def play_audio(file_path):
    try:

        with wave.open(file_path, 'rb') as wf:
            p = pyaudio.PyAudio()
            stream = p.open(
                format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True
            )
            chunk_size = 1024
            audio_data = wf.readframes(chunk_size)
            while audio_data:
                stream.write(audio_data)
                audio_data = wf.readframes(chunk_size)
            stream.stop_stream()
            stream.close()
            p.terminate()

    except Exception as e:
        print(f"An error occurred while playing the audio: {e}")

def main():
    print("Generating audio from text...")
    output_file = text_to_speech(TEXT_TO_SPEECH, LANGUAGE, OUTPUT_FILE)
    if output_file:
        print("Playing the audio...")
        play_audio(output_file)

if __name__ == "__main__":
    main()
