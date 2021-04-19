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
def main():
    data2 = pd.read_csv('data/data2.csv', sep=';')
    rev = []
    for column in data2.columns[1:]:
        rev.append(sum(data2[column]))
    arr_rev = []
    rev_sum = sum(rev)
    for i, val in enumerate(rev):
        arr_rev.append(val/rev_sum*100)

    data3 = pd.read_csv('data/data3.csv', sep=';')
    dataprogram = data3[list(data3)].values.tolist()

    return render_template('index.html', arr_rev=arr_rev, temp_arr=dataprogram)


@app.route("/pengadaan")
@nocache
def pengadaan():
    data1 = pd.read_csv('data/data1.csv', sep=';')
    datapengadaan = data1[list(data1)].values.tolist()

    return render_template('pengadaan.html', temp_arr=datapengadaan)


if __name__ == "__main__":
    app.run(debug=True)
