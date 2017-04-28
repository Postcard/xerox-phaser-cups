import os

from flask import Flask, render_template, request

import figure

from .utils import create_poster, print_to_xerox_7100N

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/print', methods=['POST'])
def _print():
    code = request.form['code']
    portrait = figure.Portrait.get(code)
    filepath = create_poster(portrait)
    print_to_xerox_7100N(filepath)
    os.remove(filepath)
    return "Printing in progress..."
