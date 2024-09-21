from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

# Use the environment variable for the Ollama API URL
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://ollama-1:11434/v1/generate') # Default to the internal service name
#API_KEY = os.environ.get("OLLAMA_API_KEY", "your_api_key")  # Use an environment variable for the API key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_input = request.form['user_input']
    
    # Send a request to the Ollama API without the Authorization header
    headers = {'Content-Type': 'application/json'}
    data = {
        "prompt": user_input,
        "max_tokens": 100,
    }
    response = requests.post(OLLAMA_API_URL, json=data, headers=headers)
    
    if response.status_code == 200:
        generated_text = response.json()['text']
        return jsonify({"generated_text": generated_text})
    else:
        return jsonify({"error": "Failed to generate text."})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # Bind to all interfaces
