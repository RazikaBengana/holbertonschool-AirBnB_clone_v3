#!/usr/bin/python3
"""Script to run a simple Flask web application"""

from flask import Flask


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """Route to return a greeting 'Hello HBNB!' when accessed at the root URL"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Route to return 'HBNB' when '/hbnb' URL is accessed"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c(text):
    """
    Display 'C' followed by the custom text;
    Text underscores are replaced by spaces
    """
    text = text.replace("_", " ")
    return "C {}".format(text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port='5000')
