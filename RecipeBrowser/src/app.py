from flask import Flask, render_template, request, jsonify
import os
import requests
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Use the environment variable for Ollama API URL; default to localhost if not set
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://127.0.0.1:11434/api/generate')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    company_name = request.form.get('company_name', 'Unknown Company')  # This should work as expected
    ingredients = request.form.get('ingredients', '')  # Update to match the form field name
    
    # Log company name and ingredients received
    app.logger.debug(f"Company Name: {company_name}")
    app.logger.debug(f"Ingredients: {ingredients}")

    # Create user input for Ollama API
    user_input = f"Company: {company_name}, Ingredients: {ingredients}"
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
            return jsonify({"response": generated_text})  # Return a 'response' key that matches your frontend
        else:
            return jsonify({"error": f"Failed to generate text. Status code: {response.status_code}, Response: {response.text}"})
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Request to Ollama API failed: {e}")
        return jsonify({"error": "Request failed."})


if __name__ == '__main__':
    app.run(debug=True)
