# Passwordless Authentication with Python 3.8 & Flask

This is an enhanced Python/Flask version of the Passwordless.dev example application. It demonstrates how to implement passwordless authentication in Python with the Flask micro-framework using Bitwarden's Passwordless API. 

This version of the application includes improvements in handling sensitive data, error handling, logging, configuration, and code organization. It also provides a scalable and maintainable code structure that can be built on and expanded.

* Please read the documentation here: [https://docs.passwordless.dev](https://docs.passwordless.dev)
* Get your own API keys here: [https://admin.passwordless.dev/signup](https://admin.passwordless.dev/signup)


## Table of Contents

1. [Overview](#overview)
2. [About Flask](#about-flask)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Setting Environment Variables](#setting-environment-variables)
6. [Running the Application](#running-the-application)
7. [Advanced Configuration](#advanced-configuration)
8. [Enhancements and Features](#enhancements-and-features)
9. [Application Flow](#application-flow)
10. [Troubleshooting](#troubleshooting)

## Overview

This application includes the following components:

- A Flask server (`app.py`) that interacts with the Passwordless API to handle user registration and sign-in operations.
- An HTML page (`public/index.html`) where users can enter their username to register or sign in.
- Two client-side JavaScript files (`public/client-register.js`, `public/client-signin.js`) that handle user interactions and communicate with the Flask server.

## About Flask
Flask, a Python micro-framework, has emerged as a preferred tool for developers as the industry pivots towards micro-services and serverless platforms. With its lightweight, intuitive, and flexible design, Flask is ideal for building scalable web applications. This is demonstrated in this Passwordless.dev example application.

Flask's simplicity allows quick start-ups, but its extensibility can support complex, database-driven web applications. Flask promotes a modular design, fitting perfectly with the microservices architecture. It excels in creating RESTful APIs, a cornerstone of microservices, with minimal code due to its intuitive routing system and request handling support. Moreover, Flask's ecosystem is rich with extensions, enhancing its versatility.

This application, utilizing Flask, highlights its capabilities. It integrates a Flask server, an HTML page for user interactions, and two client-side JavaScript files to manage these interactions and communicate with the server.

Working with lower-level libraries like Python's urllib can be complex and error-prone. Flask alleviates these challenges with its intuitive API for managing HTTP communication, a powerful routing system, and built-in support for cookies and sessions. It also integrates seamlessly with Jinja2 for template rendering and Werkzeug for HTTP and WSGI utilities, reducing the code developers need to write.

In summary, Flask minimizes coding length and effort, mitigates limitations of lower-level libraries like urllib, and provides high-level abstractions and powerful features. It's an excellent choice for building web applications in Python.

## Prerequisites

To run this application, you need:

- Python 3.8 or later
- pip (Python package installer)
- Your Passwordless API key and secret

## Installation

1. Clone or download the repository to your local machine.
2. Open a terminal and navigate to the directory containing the application.
3. Install the necessary Python packages by running:

```bash
pip install flask flask_cors requests
```

## Setting Environment Variables

Set your environment variables for `API_URL`, `API_SECRET`, `API_KEY`, and `PORT`.

### On Unix/Linux/Mac systems, you might run:

```bash
export API_URL=https://v4.passwordless.dev
export API_SECRET=your_api_secret
export API_KEY=your_api_key
export PORT=4000
```

### On Windows systems, you might run:

```cmd
set API_URL=https://v4.passwordless.dev
set API_SECRET=your_api_secret
set API_KEY=your_api_key
set PORT=4000
```
### On Windows Powershell or terminal, you might run:


```powershell
$env:API_URL="https://v4.passwordless.dev"
$env:API_SECRET="your_api_secret"
$env:API_KEY="your_api_key"
$env:PORT="your port number"
```

### In Jupyter Notebook:

```python
import os

os.environ['API_URL'] = 'https://v4.passwordless.dev'
os.environ['API_SECRET'] = 'your_api_secret'
os.environ['API_KEY'] = 'your_api_key'
os.environ['PORT'] = '4000'  # or whatever port number you want to use
```

Replace `your_api_secret` and `your_api_key` with your actual Passwordless API secret and key.

## Running the Application

1. Open the `public/index.html` file in a text editor. Replace `<YOUR_API_KEY>` with your actual API key.
2. Run the Flask app with:

```bash
python app.py
```

* Your Flask app should now be running and listening for requests on `http://localhost:4000`.
  * **You must use localhost instead of 127.0.0.1**

* Once the Flask application starts, it performs a pre-flight check to ensure the environment variables are set correctly. 
* If any of the environment variables **(API_URL, API_SECRET, API_KEY, PORT)** are not set, an error message will be printed in the console. If all the environment variables are set correctly, the Flask application will start serving requests.


## Advanced Configuration

In a production environment, you might want to consider the following advanced configuration options:

### Secure API Key Storage

Storing API keys in environment variables is simple, but it might not be the most secure method, especially for sensitive keys. Consider using a dedicated secret management service, such as AWS Secrets Manager, Google Cloud Secret Manager, or HashiCorp Vault. These services provide secure, managed storage for API keys and other secrets, and they can often be accessed directly from your application code.

Here's an example of how you can use AWS Secrets Manager to store and retrieve your Passwordless API key:

```python
import boto3
from botocore.exceptions import BotoCoreError, ClientError

def get_secret():
    secret_name = "PasswordlessAPIKey"
    region_name = "us-west-2"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise Exception("Couldn't retrieve the API key.") from e
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            raise Exception("Couldn't retrieve the API key.")
    return secret
```

Remember to replace `secret_name` and `region_name` with your secret's name and your AWS region. Then, in your code, you can call `get_secret()` to retrieve your API key.

### Scalable Server Setup

The built-in Flask server is not suitable for production use. It's intended for development and testing, and it doesn't scale well to handle large amounts of traffic. Consider using a production-ready server like Gunicorn or uWSGI, and running your Flask app behind a reverse proxy like Nginx.

Here's an example of how you can use Gunicorn:

1. Install Gunicorn:

```bash
pip install gunicorn
```

2. Run your Flask app with Gunicorn:

```bash
gunicorn -w 4 -b 127.0.0.1:4000 app:app
```

In this command, `-w 4` specifies the number of worker processes, and `-b 127.0.0.1:4000` specifies the binding address and port. `app:app` specifies the module and application (both named `app` in this case).

### Load Balancing

If your application needs to handle a lot of traffic, you might want to distribute the load across multiple servers. This can be achieved using a load balancer, which distributes incoming requests to multiple servers. This can significantly increase the capacity of your application and improve reliability.

There are many load balancers available, such as Nginx, HAProxy, and AWS Elastic Load Balancer (ELB). The configuration will depend on the specific load balancer you choose. For example, to configure Nginx as a load balancer, you would add a section like this to your Nginx configuration file:

```bash
http {
    upstream app_servers {
        server 127.0.0.1:4000;
        server 127.0.0.1:4001;
        server 127.0.0.1:4002;
    }

    server {
        listen 80;

        location / {
            proxy_pass http://app_servers;
        }
    }
}
```

In this configuration, Nginx distributes incoming requests to three instances of the application running on ports 4000, 4001, and 4002.

### Database Integration

In a real-world application, consider storing user data in a database. This would allow you to maintain user sessions, store user preferences, and perform other user-related operations. Flask can work with a variety of databases through extensions, such as Flask-SQLAlchemy for SQLAlchemy support and Flask-PyMongo for MongoDB.

Here's an example of how you can use Flask-SQLAlchemy to integrate a SQLite database with your Flask app:

1. Install Flask-SQLAlchemy:

```bash
pip install Flask-SQLAlchemy
```

2. In your Flask app, set up the SQLAlchemy engine and define your model:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
```

3. Create the database tables:

```python
db.create_all()
```

4. Now you can create, retrieve, update, and delete users in your database:

```python
# Create a new user
user = User(username='flask')
db.session.add(user)
db.session.commit()

# Retrieve a user
user = User.query.filter_by(username='flask').first()

# Update a user
user.username = 'new-username'
db.session.commit()

# Delete a user
db.session.delete(user)
db.session.commit()
```

Remember to replace `'sqlite:////tmp/test.db'` with your actual database URL.

## Enhancements and Features

This version of the application includes several enhancements and features compared to the original code:

- **Environment variables**: Using environment variables for configuration settings, like your API keys, is a good practice for keeping your secrets safe and your code flexible across different environments.
- **Logging**: Using the logging module to handle all your logging needs is a good practice. It allows you to control the level of logging, and it logs the timestamp and other useful information along with your messages.
- **Error handling**: Having custom error handlers for your Flask app allows you to control what happens when an error occurs, and how that is communicated back to the user.
- **Modular code**: The create_app function is a common pattern in Flask applications. It allows for better organization of your code, and it makes it easier to scale and maintain your application.
- **Separate function for API requests**: The make_api_request function is a good example of code reuse. It reduces duplication and makes the code cleaner and easier to manage.
- **HTTP Verbs**: In your '/create-token' route, the POST method is used to create resources, according to HTTP verb semantics.
- **SSL Verification**: SSL verification is enabled in your API calls to ensure security.
- **Flask application instance**: The application factory pattern that Flask recommends is used.
- **Return statements**: In Flask, you can return a tuple where the first element is the response body, and the second element is the status code. If the status code is not 200, you should return an error message along with the appropriate error status code.

## Application Flow

The application uses a Flask server, an HTML interface, and two JavaScript files to handle user registration and login.

1. **Index Page**: The user interacts with the `index.html` page, which makes use of two JavaScript files, `client-register.js` and `client-signin.js`, to manage user interactions and make AJAX calls to the Flask server.

2. **Client-Side JavaScript**: The `client-register.js` and `client-signin.js` files send AJAX requests to the Flask server. The server then handles these requests, interacts with the Passwordless API, and sends a response back to the client.

3. **Flask Server**: The Flask server (`app.py`) handles the requests from the client-side JavaScript. It interacts with the Passwordless API, processes the API responses, and sends the results back to the client.

## Troubleshooting

If you encounter issues while setting up or running the application, the following steps might help:

- **Issue: Python or pip is not recognized as a command.**
  - Solution: This likely means that Python or pip is not installed or not added to your PATH. Make sure you have Python 3.8 or later installed and that both Python and pip are added to your PATH.

- **Issue: Error while installing the Python packages.**
  - Solution: If you're seeing permission errors while trying to install the packages, try using the `--user` flag with the pip command (`pip install --user flask flask_cors requests`). If you're seeing a "not found" error for a package, make sure you have spelled the package name correctly.

- **Issue: The Flask app cannot be started, or is not accessible at http://localhost:4000.**
  - Solution: Make sure the `PORT` environment variable is set to `4000` or to the port you want the Flask app to run on. If the `PORT` variable is set correctly, make sure no other processes are using the port.

- **Issue: Error messages related to the Passwordless API (e.g., "ApiSecret is required").**
  - Solution: Make sure you have set the `API_SECRET` and `API_KEY` environment variables to your actual Passwordless API secret and key. If you're seeing a different error from the Passwordless API, refer to the Passwordless API documentation for more information.

- **Issue: The web page is not loading, or the JavaScript functionality is not working.**
  - Solution: Make sure your Flask server is running and accessible. If it is, check the JavaScript console in your browser for error messages. The issue could be related to the JavaScript code, the Flask server, or the communication between them.

If you're still encountering issues after trying these steps, you might want to seek help from the community or a developer with experience in Python, Flask, and JavaScript.