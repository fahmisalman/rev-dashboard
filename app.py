from flask import Flask, render_template, make_response
from functools import wraps, update_wrapper
import pandas as pd
from datetime import datetime
import numpy as np
import os

app = Flask(__name__)

IMAGE_FOLDER = os.path.join('static', 'img')
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)


@app.route("/")
@nocache
def main(year=2021):
    # Pie chart

    print(year)
    data2 = pd.read_csv('data/data2.csv', sep=';')
    rev = []
    for column in data2.columns[1:]:
        rev.append(sum(data2[column]))
    arr_rev = []
    rev_sum = sum(rev)
    for i, val in enumerate(rev):
        arr_rev.append(val/rev_sum*100)

    temp_arr = [
        ['1', '1', '1', '1', '1', '1', '1', '1', '1'],
        ['2', '2', '2', '2', '2', '2', '2', '2', '2']
    ]

    return render_template('index.html', arr_rev=arr_rev, temp_arr=temp_arr)


@app.route("/pengadaan")
@nocache
def pengadaan():
    # Pie chart
    data2 = pd.read_csv('data/data2.csv', sep=';')
    rev = []
    for column in data2.columns[1:]:
        rev.append(sum(data2[column]))
    arr_rev = []
    rev_sum = sum(rev)
    for i, val in enumerate(rev):
        arr_rev.append(val/rev_sum*100)

    return render_template('pengadaan.html')


if __name__ == "__main__":
    app.run(debug=True)
