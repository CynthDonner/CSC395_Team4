from flask import Flask, render_template, request, jsonify
import os
import requests
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Use the environment variable for Ollama API URL
OLLAMA_API_URL = 'http://127.0.0.1:11434/api/generate'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_input = request.form['user_input']
    app.logger.debug(f"User input received: {user_input}")

    headers = {'Content-Type': 'application/json'}
    data = {
        "model": "llama3.1",
        "prompt": user_input,
        "max_tokens": 100,
        "stream": False
    }

    app.logger.debug(f"Sending request to Ollama API at {OLLAMA_API_URL} with data: {data}")

    try:
        response = requests.post(OLLAMA_API_URL, json=data, headers=headers)
        app.logger.debug(f"Response status code: {response.status_code}")

        # Log the full response content
        app.logger.debug(f"Response content: {response.text}")

        if response.status_code == 200:
            generated_text = response.json().get('response', 'No response')
            return jsonify({"generated_text": generated_text})
        else:
            return jsonify({"error": f"Failed to generate text. Status code: {response.status_code}, Response: {response.text}"})
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Request to Ollama API failed: {e}")
        return jsonify({"error": "Request failed."})

if __name__ == '__main__':
    app.run(debug=True)
