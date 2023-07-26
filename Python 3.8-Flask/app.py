from flask import Flask, request, send_from_directory
from flask_cors import CORS
import os
import requests
import random
import json

app = Flask(__name__, static_folder='public')
CORS(app) # This will enable CORS for all routes

# Load environment variables
API_URL = os.getenv('API_URL', 'https://v4.passwordless.dev')
API_SECRET = os.getenv('API_SECRET', 'YOUR_API_SECRET') # Replace with your API secret
API_KEY = os.getenv('API_KEY', 'YOUR_API_KEY') # this will be injected to index.html
PORT = int(os.getenv('PORT', 3000))

# Print out the API URL, key, and secret for debugging purposes
print(f"Using API URL: {API_URL}")
print(f"Using API key: {API_KEY}")
print(f"Using API secret: {API_SECRET}")

@app.route('/create-token', methods=['GET'])
def create_token():
    """Register - Get token from the passwordless API"""
    try:
        userId = getRandomInt(999999999)
        alias = request.args.get('alias')
        displayname = "Mr Guest"
        payload = {
            'userId': userId,
            'username': alias or displayname,
            'displayname': displayname,
            'aliases': [alias] if alias else [] # We can also set aliases for the userid, so that signin can be initiated without knowing the userid
        }
        response = requests.post(
            API_URL + "/register/token",
            headers={'ApiSecret': API_SECRET, 'Content-Type': 'application/json'},
            json=payload,
            verify=False # This is equivalent to 'rejectUnauthorized: false' in the Node.js version. In a production environment, you should probably set this to True.
        )
        response_data = response.json()
        if response.status_code != 200:
            print(f"Error in /create-token: {response_data}")
        return (response_data, response.status_code)
    except Exception as e:
        print(f"Exception in /create-token: {str(e)}")
        return ({"error": "Exception occurred"}, 500)

@app.route('/verify-signin', methods=['GET'])
def verify_signin():
    """Sign in - Verify the sign in"""
    try:
        token = {'token': request.args.get('token')}
        response = requests.post(
            API_URL + "/signin/verify",
            headers={'ApiSecret': API_SECRET, 'Content-Type': 'application/json'},
            json=token,
            verify=False # This is equivalent to 'rejectUnauthorized: false' in the Node.js version. In a production environment, you should probably set this to True.
        )
        body = response.json()
        if response.status_code != 200:
            print(f"Error in /verify-signin: {body}")
        return (body, response.status_code)
    except Exception as e:
        print(f"Exception in /verify-signin: {str(e)}")
        return ({"error": "Exception occurred"}, 500)

@app.route('/')
def index():
    """Small helper to update API_KEYs: Response with index.html but replace API_KEY value."""
    try:
        with open('public/index.html', 'r') as file:
            data = file.read()
        result = data.replace('<YOUR_API_KEY>', API_KEY)
        return result
    except Exception as e:
        print(f"Exception in index route: {str(e)}")
        return ({"error": "Exception occurred"}, 500)

@app.route('/<path:path>')
def static_file(path):
    """Serve static files from the 'public' directory"""
    try:
        return send_from_directory('public', path)
    except Exception as e:
        print(f"Exception in static file route: {str(e)}")
        return ({"error": "Exception occurred"}, 500)

def getRandomInt(max):
    """Helper function to generate a random integer"""
    return random.randint(0, max)

if __name__ == '__main__':
    try:
        app.run(port=PORT)
    except Exception as e:
        print(f"Exception in main: {str(e)}")
