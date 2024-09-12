import os
import requests
from flask import Flask, request, jsonify
from gradio_client import Client, file

app = Flask(__name__)

# Get the directory where app.py is located
APP_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/voice-clone', methods=['POST'])
def voice_clone():
    data = request.json

    text = data.get('text', 'Hello!!')
    audio_url = data.get('audio_url')

    if not audio_url:
        return jsonify({"error": "Audio URL is required"}), 400

    # try:
    client = Client("tonyassi/voice-clone")
    result = client.predict(
        text=text,
        audio=file(audio_url),
        api_name="/predict"
    )
    # Enhanced logging of the result type and content
    result_type = type(result)
    print(f"Result Type: {result_type}")
    print(f"Result Content: {result}")
    # Define the output file path in the same directory as app.py
    output_path = os.path.join(APP_DIR, "output.wav")
    if isinstance(result, str):
        if result.startswith("http"):
            # Download the file from the URL
            response = requests.get(result)
            with open(output_path, 'wb') as f:
                f.write(response.content)
        else:
            # Handle non-URL string result
            print(f"Received a non-URL string: {result}")
            with open(output_path, 'w') as f:
                f.write(result)
    elif isinstance(result, bytes):
        # Save binary result directly
        with open(output_path, 'wb') as f:
            f.write(result)
    elif isinstance(result, list):
        # Handle list result (e.g., if it's a list of audio segments)
        print(f"Received a list result with {len(result)} items")
        if all(isinstance(item, bytes) for item in result):
            with open(output_path, 'wb') as f:
                for item in result:
                    f.write(item)
        else:
            return jsonify({
                "error": "Unexpected list content",
                "result_content": str(result)
            }), 500
    else:
        # Log unexpected format for debugging
        return jsonify({
            "error": "Unexpected result format",
            "result_type": str(result_type),
            "result_content": str(result)
        }), 500

        return jsonify({"output_file": output_path})

    # except Exception as e:
    #     print(f"Exception occurred: {str(e)}")
    #     return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)