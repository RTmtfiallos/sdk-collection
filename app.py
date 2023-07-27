#!/usr/bin/env python
# coding: utf-8

from flask import Flask, request, send_from_directory
from flask_cors import CORS
import os
import requests
import random
import json
import logging

class ApiError(Exception):
    """A custom exception for API errors."""
    pass

def create_app():
    app = Flask(__name__, static_folder='public')
    CORS(app) # This will enable CORS for all routes

    # Setup logging
    logging.basicConfig(level=logging.INFO)  # or DEBUG, ERROR, WARNING

    # Load environment variables
    API_URL = os.getenv('API_URL') # Removed the default value
    API_SECRET = os.getenv('API_SECRET') # Removed the default value
    API_KEY = os.getenv('API_KEY') # Removed the default value
    
    # Get the PORT environment variable and set a default value if it's not set
    PORT = int(os.getenv('PORT', '3000'))  # Convert the port number back to an integer
   
    # Check that the required environment variables are set
    if API_URL is None or API_SECRET is None or API_KEY is None:
        raise ValueError("API_URL, API_SECRET, and API_KEY must be set.")

    # Print out the API URL, key, and secret for debugging purposes
    logging.info(f"Using API URL: {API_URL}")
    logging.info(f"Using API key: {API_KEY}")
    logging.info(f"Using API secret: {API_SECRET}")

    def make_api_request(url, headers, payload=None, method='POST'):
        """Make a POST or GET request to the specified API URL with the provided headers and payload.
        
        Inputs:
        url (str): The URL to make the POST request to.
        headers (dict): The headers to include in the request.
        payload (dict): The payload to include in the request.
        method (str): The HTTP method to use for the request. Default is 'POST'.
        
        Outputs:
        A tuple containing the response data and the status code.
        """
        try:
            if method == 'POST':
                response = requests.post(
                    url,
                    headers=headers,
                    json=payload
                )
            elif method == 'GET':
                response = requests.get(
                    url,
                    headers=headers,
                    params=payload
                )
            else:
                raise ValueError("Invalid method: must be 'POST' or 'GET'.")

            response_data = response.json()
            if response.status_code != 200:
                logging.error(f"Error in API request to {url}: {response_data}")
                raise ApiError(f"API request failed with status {response.status_code}")
            logging.info(f"Successful API request to {url}")
            return (response_data, response.status_code)
        except Exception as e:
            logging.exception(f"Exception in API request to {url}: {str(e)}")
            return ({"error": "Exception occurred"}, 500)

    @app.route('/create-token', methods=['POST', 'GET'])
    def create_token():
        """Register - Get token from the passwordless API.
        
        This endpoint creates a token by making a POST request to the /register/token endpoint of the API.
        The token is created for a user with a unique userId, and an alias if provided in the request parameters.
        
        Inputs:
        alias (str): An optional alias for the user. If not provided, the username and display name will be 'Mr Guest'.
        
        Outputs:
        A tuple containing the response data and the status code.
        """
        userId = getRandomInt(999999999)
        alias = request.args.get('alias')
        displayname = "Mr Guest"
        payload = {
            'userId': userId,
            'username': alias or displayname,
            'displayname': displayname,
            'aliases': [alias] if alias else [] # We can also set aliases for the userid, so that signin can be initiated without knowing the userid
        }
        headers = {'ApiSecret': API_SECRET, 'Content-Type': 'application/json'}
        return make_api_request(API_URL + "/register/token", headers, payload)

    @app.route('/verify-signin', methods=['GET'])
    def verify_signin():
        """Sign in - Verify the sign in.
        
        This endpoint verifies a sign in attempt by making a POST request to the /signin/verify endpoint of the API.
        The sign in attempt is verified using a token provided in the request parameters.
        
        Inputs:
        token (str): The token used to verify the sign in attempt.
        
        Outputs:
        A tuple containing the response body and the status code.
        """
        token = {'token': request.args.get('token')}
        headers = {'ApiSecret': API_SECRET, 'Content-Type': 'application/json'}
        return make_api_request(API_URL + "/signin/verify", headers, token)

    @app.route('/')
    def index():
        """Small helper to update API_KEYs: Response with index.html but replace API_KEY value.
        
        This endpoint serves the index.html file in the 'public' directory, after replacing '<YOUR_API_KEY>' with the actual API key.
        
        Outputs:
        The contents of the index.html file, with '<YOUR_API_KEY>' replaced by the actual API key.
        """
        try:
            with open('public/index.html', 'r') as file:
                data = file.read()
            result = data.replace('<YOUR_API_KEY>', API_KEY)
            logging.info("Successfully served index.html")
            return result
        except Exception as e:
            logging.exception(f"Exception in index route: {str(e)}")
            return ({"error": "Exception occurred"}, 500)

    @app.route('/<path:path>')
    def static_file(path):
        """Serve static files from the 'public' directory
        
        This endpoint serves static files from the 'public' directory. The specific file to serve is determined by the 'path' parameter.
        
        Inputs:
        path (str): The path to the file in the 'public' directory that should be served.
        
        Outputs:
        The requested file from the 'public' directory.
        """
        try:
            logging.info(f"Successfully served file: {path}")
            return send_from_directory('public', path)
        except Exception as e:
            logging.exception(f"Exception in static file route: {str(e)}")
            return ({"error": "Exception occurred"}, 500)

    def getRandomInt(max):
        """Helper function to generate a random integer
        
        This function generates a random integer between 0 and the input 'max'.
        
        Inputs:
        max (int): The maximum value for the random integer.
        
        Outputs:
        A random integer between 0 and 'max'.
        """
        return random.randint(0, max)

    @app.errorhandler(404)
    def not_found(error):
        """Custom error handler for 404 errors"""
        return ({"error": "Not found"}, 404)

    @app.errorhandler(500)
    def internal_error(error):
        """Custom error handler for 500 errors"""
        return ({"error": "Internal server error"}, 500)

    return app, PORT

if __name__ == '__main__':
    app, PORT = create_app()  # Unpack both the app and PORT from the create_app function
    try:
        app.run(port=PORT)  # Use PORT here
    except Exception as e:
        logging.exception(f"Exception in main: {str(e)}")


# In[ ]:




