from flask import Flask, request, jsonify
from TTS.api import TTS
import os
import requests

# Ensure Coqui terms of service are agreed
os.environ["COQUI_TOS_AGREED"] = "1"

app = Flask(__name__)

# Load the TTS model
device = "cuda"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Function to download the file from URL
def download_file(url, save_path):
    try:
        response = requests.get(url)
        with open(save_path, 'wb') as file:
            file.write(response.content)
        return save_path
    except Exception as e:
        raise Exception(f"Error downloading file: {e}")

# Function to perform voice cloning and generate audio
def clone(text, speaker_wav_path):
    output_path = "./output.wav"  # Output file path
    tts.tts_to_file(text=text, speaker_wav=speaker_wav_path, language="en", file_path=output_path)
    return output_path

# API route for cloning the voice
@app.route('/clone', methods=['POST'])
def clone_voice():
    data = request.get_json()
    text = data.get('text')
    audio_path = data.get('audio_path')  # Path to the speaker's audio file
    audio_url = data.get('audio_url')  # URL to the speaker's audio file

    if not text or (not audio_path and not audio_url):
        return jsonify({"error": "Text and either audio_path or audio_url is required"}), 400
    
    try:
        if audio_url:
            # Download audio from the URL
            downloaded_path = "./downloaded_speaker.wav"
            audio_path = download_file(audio_url, downloaded_path)
        
        output_file = clone(text, audio_path)  # Call the clone function
        return jsonify({"output_file": output_file})  # Return the output file path
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
