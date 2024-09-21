from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_API_URL = "https://api.ollama.com/v1/generate"  # Replace with actual API endpoint
API_KEY = "your_api_key"  # Replace with your Ollama API key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_input = request.form['user_input']
    
    # Send a request to the Ollama API
    headers = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}
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
    app.run(debug=True)
