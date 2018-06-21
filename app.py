from flask import Flask,render_template,request,redirect
import numpy as np
import os
import quandl
import datetime
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN

app = Flask(__name__)


def datetime(x):
    return np.array(x, dtype=np.datetime64)

@app.route('/index',methods=['GET','POST'])
def index():
  if request.method=="GET":
    return render_template('choose_stock.html')

  else:
    ticker_sym=request.form['ticker']
    price=request.form['features']
    quandl.ApiConfig.api_key = 'uMFrusZD9H5V3e2uJ59A'
    data = quandl.get_table('WIKI/PRICES', ticker = ticker_sym, qopts = { 'columns': ['date',price]}, date = { 'gte': '2017-05-10', 'lte': '2017-06-10' }, paginate=True)
    p1 = figure(x_axis_type="datetime", title="Stock Prices")
    p1.grid.grid_line_alpha=0.3
    p1.xaxis.axis_label = 'Date'
    p1.yaxis.axis_label = 'Price'

    p1.line(data['date'], data[request.form['features']], color='#A6CEE3', legend=price)

    script, div = components(p1)
    cdn_js=CDN.js_files[0]
    cdn_css=CDN.css_files[0]

    return render_template('plot.html',ticker=ticker_sym,script=script,div=div,cdn_css=cdn_css,cdn_js=cdn_js)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
