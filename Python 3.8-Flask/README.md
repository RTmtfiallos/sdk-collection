# Passwordless Authentication with Python 3.8 & Flask

This is a Python/Flask version of the Passwordless.dev example application. It demonstrates how to implement passwordless authentication in a Flask web application using the Passwordless API.

* Please read the documentation here: https://docs.passwordless.dev
* Get your own API keys here: https://admin.passwordless.dev/signup


## Overview

This application includes the following components:

1. A Flask server that interacts with the Passwordless API to handle user registration and sign-in operations.
2. An HTML page where users can enter their username to register or sign in.
3. Two client-side JavaScript files that handle user interactions and communicate with the Flask server.

## Prerequisites

To run this application, you need:

- Python 3.8 or later
- pip (Python package installer)
- Your Passwordless API key and secret

## Installation

There are two ways to install and use this application:

### Option 1: Using pip

This application is available as a Python package and can be installed via pip:

```bash
pip install passwordless-flask
```

After installation, you can use the application in your Python scripts:

```python
import passwordless_flask as pf

# Configure the API keys and URLs
pf.configure(api_url, api_secret, api_key, port)

# Start the server
pf.start_server()
```

Replace `api_url`, `api_secret`, `api_key`, and `port` with your actual API URL, secret, key, and the port you want the server to run on.

### Option 2: Manual Installation

1. Clone or download the repository to your local machine.

2. Open a terminal and navigate to the directory containing the application.

3. Install the necessary Python packages by running:

    ```bash
    pip install flask flask_cors requests
    ```

4. Set your environment variables for `API_URL`, `API_SECRET`, and `API_KEY`. You can do this in the terminal before you run your app. On a Unix/Linux/Mac system, you might run:

    ```bash
    export API_URL=https://v4.passwordless.dev
    export API_SECRET=your_api_secret
    export API_KEY=your_api_key
    ```

    On a Windows system, you might run:

    ```cmd
    set API_URL=https://v4.passwordless.dev
    set API_SECRET=your_api_secret
    set API_KEY=your_api_key
    ```

    Replace `your_api_secret` and `your_api_key` with your actual Passwordless API secret and key.

5. Open the `public/index.html` file in a text editor. Replace `<YOUR_API_KEY>` with your actual API key.

6. Run the Flask app with:

    ```bash
    python app.py
    ```

Your Flask app should now be running and listening for requests on `http://localhost:3000`.

## Advanced Configuration

In a production environment, you might want to consider the following advanced configuration options:

### Secure API Key Storage

Storing API keys in environment variables is simple, but it might not be the most secure method, especially for sensitive keys. Consider using a dedicated secret management service, such as AWS Secrets Manager, Google Cloud Secret Manager, or HashiCorp Vault. These services provide secure, managed storage for API keys and other secrets, and they can often be accessed directly from your application code.

### Scalable Server Setup

The built-in Flask server is not suitable for production use. It's intended for development and testing, and it doesn't scale well to handle large amounts of traffic. Consider using a production-ready server like Gunicorn or uWSGI, and running your Flask app behind a reverse proxy like Nginx.

### Load Balancing

If your application needs to handle a lot of traffic, you might want to distribute the load across multiple servers. This can be achieved using a load balancer, which distributes incoming requests to multiple servers. This can significantly increase the capacity of your application and improve reliability.

### Database Integration

In this example, user information is not stored in a database, but in a real-world application, you might want to store user data in a database. This would allow you to maintain user sessions, store user preferences, and perform other user-related operations. Flask can work with a variety of databases through extensions, such as Flask-SQLAlchemy for SQLAlchemy support and Flask-PyMongo for MongoDB.

## Using the Application

Open your web browser and navigate to `http://localhost:3000`. Enter a username in the text field and click the "Register" button to register a new user, or the "Login" button to sign in an existing user.

The application will communicate with the Passwordless API to register a passkey for the username or verify a sign-in operation. You can view the result of the operation on the web page.

## Troubleshooting

If you encounter issues while setting up or running the application, the following steps might help:

1. **Issue: Python or pip is not recognized as a command.**
   - Solution: This likely means that Python or pip is not installed or not added to your PATH. Make sure you have Python 3.8 or later installed

 and that both Python and pip are added to your PATH.

2. **Issue: Error while installing the Python packages.**
   - Solution: If you're seeing permission errors while trying to install the packages, try using the `--user` flag with the pip command (`pip install --user flask flask_cors requests`). If you're seeing a "not found" error for a package, make sure you have spelled the package name correctly.

3. **Issue: The Flask app cannot be started, or is not accessible at http://localhost:3000.**
   - Solution: Make sure the PORT environment variable is set to 3000 or to the port you want the Flask app to run on. If the PORT variable is set correctly, make sure no other processes are using the port.

4. **Issue: Error messages related to the Passwordless API (e.g., "ApiSecret is required").**
   - Solution: Make sure you have set the API_SECRET and API_KEY environment variables to your actual Passwordless API secret and key. If you're seeing a different error from the Passwordless API, refer to the [Passwordless API documentation](https://docs.passwordless.dev/) for more information.

5. **Issue: The web page is not loading, or the JavaScript functionality is not working.**
   - Solution: Make sure your Flask server is running and accessible. If it is, check the JavaScript console in your browser for error messages. The issue could be related to the JavaScript code, the Flask server, or the communication between them.

If you're still encountering issues after trying these steps, you might want to seek help from the community or a developer with experience in Python, Flask, and JavaScript.
