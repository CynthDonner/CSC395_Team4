from flask import Flask, render_template, request, jsonify
import os
import requests
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Use the environment variable for Ollama API URL; default to localhost if not set
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://127.0.0.1:11434/api/generate')


initial_context = '''
"You are an AI that helps analyze ingredients provided by companies for creating recipes. "
        "When given a company and a list of ingredients, generate a recipe, generally
        in the form of a popular food or dessert, using the ingredients listed, 
        and then add new ingredients to the recipe that are from the given company.
        For example, if you got a list of ingredients like ketchup, lettuce, pickles, onions, 
        cheese, you would respond with a burger recipe using new ingredients from the company
        or if the list of ingredients was baking powder, baking soda, egg, strawberry, you 
        would respond with a strawberry shortcake recipe.
        The ingredients given to you should not be from the company listed, only additions
        should be from the given company." 
        "Your response should consist of three parts, in this format.\n
        Name: (And then come up with a name for the recipe)\n
        Tagline: (A simple, catchy tagline)\n
        Recipe: (A bulleted list of each ingredient needed)"
        "Nothing else needs to be added, only return the three sections given, in the format given. 
        Make sure to always write Name: Tagline: and Recipe: in their respective sections, 
        and create a new line between each"
        "Here is the input:\n"
'''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    company_name = request.form.get('company_name', 'Unknown Company')  # Get the company name from the form
    ingredients = request.form.get('ingredients', '')  # Get the ingredients from the form
    
    # Log company name and ingredients received
    app.logger.debug(f"Company Name: {company_name}")
    app.logger.debug(f"Ingredients: {ingredients}")

    # Combine the initial context with user input
    user_input = f"Company: {company_name}, Ingredients: {ingredients}"
    full_prompt = initial_context + user_input  # Combine the context and the user's input
    
    # Log the combined prompt for debugging
    app.logger.debug(f"Full prompt sent to API: {full_prompt}")

    headers = {'Content-Type': 'application/json'}
    data = {
        "model": "llama3.1",
        "prompt": full_prompt,  # Send the full prompt including the system context
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
