"test_integration.py"
import unittest
import json
from app import app  # Import the Flask app
import requests

class TestIntegration(unittest.TestCase):
    
    def setUp(self):
        # Set up a Flask test client
        self.app = app.test_client()
        self.app.testing = True  # Set the Flask app in testing mode

    def test_integration_with_server(self):
        # Set up the test URL for the Flask app
        url = '/generate'  # This matches your route in app.py
        headers = {'Content-Type': 'application/json'}
        
        # Create the JSON payload that mimics user input
        payload = {
            "user_input": "Tell me a recipe for chocolate cake."
        }
        
        # Send POST request to the Flask server
        response = self.app.post(url, headers=headers, data=json.dumps(payload))
        
        # Check if the response from Flask server is successful (HTTP 200)
        self.assertEqual(response.status_code, 200)
        
        # Check if the response contains expected content from Ollama
        # Modify this according to what you expect the Ollama API to return
        expected_text = "Here's a great recipe for chocolate cake"
        self.assertIn(expected_text, response.json['generated_text'])

if __name__ == '__main__':
    unittest.main()