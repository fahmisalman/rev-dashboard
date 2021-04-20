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
    data2 = pd.read_csv('data/klasifikasi_kegiatan.csv', sep=';')
    labels = list(data2['Row Labels'])
    rev = list(data2['Sum of Revisi Akhir'])

    data4 = pd.read_csv('data/perubahan_anggaran.csv', sep=';')
    sum_header = list(data4)
    sum_data = data4[list(data4)].values.tolist()[0]

    data3 = pd.read_csv('data/realisasi.csv', sep=';')
    dataprogramheader = list(data3)

    data3 = data3.query('Tahun<2026 and Tahun>2019')
    dataprogram = data3[list(data3)].values.tolist()

    return render_template('index.html',
                           arr_rev=rev,
                           labels=labels,
                           sum_header=sum_header,
                           sum_data=sum_data,
                           dataprogram=dataprogram,
                           dataprogramheader=dataprogramheader,
                           dataprogramlength=len(dataprogram))


@app.route("/pengadaan")
@nocache
def pengadaan():
    data1 = pd.read_csv('data/pengadaan.csv', sep=';')
    datapengadaanheader = list(data1)

    data1 = data1.query('Tahun<2026')
    datapengadaan = data1[list(data1)].values.tolist()

    return render_template('pengadaan.html',
                           datapengadaan=datapengadaan,
                           datapengadaanheader=datapengadaanheader,
                           datapengadaanlength=len(datapengadaan))


if __name__ == "__main__":
    app.run(debug=True)
