import unittest
from unittest.mock import patch
from app import app
#from src.app import app # Import Flask app
import requests

class TestUnit(unittest.TestCase):

    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.requests.post')  # Mock the requests.post method
    def test_valid_json_input(self, mock_post):
        # Define the mock response for the requests.post call portion
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'response': "Here's a great recipe for chocolate cake using cocoa powder and sugar."
        }

        # Simulate sending valid form payload to the Flask server
        payload = {
            "user_input": "Tell me a recipe for chocolate cake"
        }
        
        # Send POST request using Flask's test client
        response = self.app.post('/generate', data=payload)

        # Check the response status
        self.assertEqual(response.status_code, 200)

        # Check the response data
        response_data = response.get_json()
        self.assertIn("response", response_data)
        self.assertEqual(response_data["response"], "Here's a great recipe for chocolate cake using cocoa powder and sugar.")

    def test_invalid_json_input(self):
        # Simulate sending invalid form payload to the Flask server
        payload = {
            "company_name": "Unknown",
            "ingredients": ""  # Invalid ingredients
        }

        # Send POST request using Flask's test client
        response = self.app.post('/generate', data=payload)

        # Check the response status
        self.assertEqual(response.status_code, 200)

        # Check the response data for error message
        response_data = response.get_json()
        self.assertIn("error", response_data)
        self.assertEqual(response_data["error"], "Request failed.")

    @patch('app.requests.post')  # Mock the requests.post method to simulate a connection failure
    def test_ollama_connection_failure(self, mock_post):
        # Simulate a connection failure
        mock_post.side_effect = requests.exceptions.ConnectionError("Connection failed")

        # Simulate sending valid form payload to the Flask server
        payload = {
            "company_name": "Test Company",
            "ingredients": "salt, pepper"
        }
        
        # Send POST request using Flask's test client
        response = self.app.post('/generate', data=payload)

        # Check the response status
        self.assertEqual(response.status_code, 200)

        # Check the response data for connection error
        response_data = response.get_json()
        self.assertIn("error", response_data)
        self.assertEqual(response_data["error"], "Request failed.")

if __name__ == '__main__':
    unittest.main()