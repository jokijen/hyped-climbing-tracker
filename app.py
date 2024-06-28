"""
This module initialises the Flask app and sets the secret key
"""
from os import getenv
from flask import Flask


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes


if __name__== "__main__":
    app.run(debug=True)
