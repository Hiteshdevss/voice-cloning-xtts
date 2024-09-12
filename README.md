# Voice Cloning API with Flask

This project implements a Flask API for voice cloning using the Gradio client. The API allows you to send text and an audio URL via JSON, and it returns the voice-cloned audio result.

## Features

- Voice cloning using the Gradio client
- Accepts JSON input for text and audio URL
- Secure with SSL (when `DEBUG_MODE` is `false`)
- CORS support for specified origins

## Prerequisites

- Python 3.7+
- [Flask](https://pypi.org/project/Flask/)
- [Pydantic](https://pypi.org/project/pydantic/)
- [Gradio Client](https://gradio.app/client)
- [boto3](https://pypi.org/project/boto3/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/voice-cloning-flask.git
    cd voice-cloning-flask
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file to store your environment variables:

    ```env
    DEBUG_MODE=true  # Set to false in production
    ```

## Running the API

To start the API, run the following command:

```bash
python app.py
