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


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python(text="is cool"):
    """
    Route to display 'Python' followed by the value of the text variable,
    with underscores replaced by spaces;
    Defaults to 'Python is cool' if no text is given
    """
    text = text.replace("_", " ")
    return "Python {}".format(text)


@app.route("/number/<int:n>", strict_slashes=False)
def number(n):
    """Route that displays a number and confirms that it is indeed a number"""
    return "{} is a number".format(n)


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    """
    Route that renders an HTML template displaying a number passed as parameter;
    It confirms it is a number using a custom template
    """
    return render_template("5-number.html", n=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_odd_or_even(n):
    """
    Route that renders an HTML template indicating whether the given number is odd or even;
    It uses a custom template to display this information
    """
    return render_template("6-number_odd_or_even.html", n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port='5000')
