"test_integration.py"
import unittest
from unittest.mock import patch
from app import app  # Import your Flask app

class TestIntegration(unittest.TestCase):
    
    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.requests.post')  # Mock the requests.post method from your app module
    def test_integration_with_server(self, mock_post):
        # Define the mock response for the requests.post call
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'response': "Here's a great recipe for chocolate cake using cocoa powder and sugar."
        }

        # Simulate sending a form payload to the Flask server
        payload = {
            "user_input": "Tell me a recipe for chocolate cake."
        }
        
        # Send POST request using Flask's test client
        response = self.app.post('/generate', data=payload)

        # Check the response status
        self.assertEqual(response.status_code, 200)

        # Check the response data
        response_data = response.get_json()
        self.assertIn("generated_text", response_data)
        self.assertEqual(response_data["generated_text"], "Here's a great recipe for chocolate cake using cocoa powder and sugar.")

if __name__ == '__main__':
    unittest.main()
