from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

IMAGE_FOLDER = os.path.join('static', 'img')
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER


@app.route("/")
def main():
    return render_template('index.html', trait='test')


if __name__ == "__main__":
    app.run(debug=True)
