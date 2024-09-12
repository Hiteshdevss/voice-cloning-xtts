from flask import Flask, request, jsonify
from TTS.api import TTS
import os

# Ensure Coqui terms of service are agreed
os.environ["COQUI_TOS_AGREED"] = "1"

app = Flask(__name__)

# Load the TTS model
device = "cuda"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Function to perform voice cloning and generate audio
def clone(text, speaker_wav_path):
    output_path = "./output.wav"  # Output file path
    tts.tts_to_file(text=text, speaker_wav=speaker_wav_path, language="en", file_path=output_path)
    return output_path

# API route for cloning the voice
@app.route('/clone', methods=['POST'])
def clone_voice():
    data = request.get_json()  # Get the JSON payload from the request
    text = data.get('text')
    audio_path = data.get('audio_path')  # Path to the speaker's audio file

    if not text or not audio_path:
        return jsonify({"error": "Text and audio_path are required"}), 400
    
    try:
        output_file = clone(text, audio_path)  # Call the clone function
        return jsonify({"output_file": output_file})  # Return the output file path
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
