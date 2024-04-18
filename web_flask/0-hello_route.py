#!/usr/bin/python3
"""Script to run a simple Flask web application"""

from flask import Flask


# Create a Flask application instance
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Route to respond with 'Hello HBNB!' when accessed at the root URL"""
    return "Hello HBNB!"


# Run the Flask application only if the script is executed directly
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
