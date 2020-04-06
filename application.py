from flask import Flask,render_template,request,redirect
import pandas as pd
#import numpy as np
import os
import io
import requests
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.tickers import DaysTicker

#from bokeh.io import show, output_notebook

app_tickers = Flask(__name__)

app_tickers.code='AAPL' #we default to the apple code


@app_tickers.route('/index_ticker',methods=['GET','POST'])
def index_ticker(): # in this function we pull the name of the ticker
    # this is a comment, just like in Python
    # note that the function name and the route argument
    # do not need to be the same.
    if request.method == 'GET':
        return render_template('tickerinfo.html')
    else:
    	#request was a POST
        app_tickers.code = request.form['ticker_code']

        return redirect('/main_ticker')

@app_tickers.route('/main_ticker')
def main_ticker2(): #in this function we create the plot

    ticker_url="https://www.quandl.com/api/v3/datatables/WIKI/PRICES.csv?ticker="+app_tickers.code+"&qopts.columns=ticker,date,close&api_key=k-cosu3xFdf6umCQSiGy"
    all_data=requests.get(ticker_url)
    raw_data = pd.read_csv(io.StringIO(all_data.content.decode('utf-8'))) #this dataframe contains all the prices for our ticker
    
    raw_data['day']=pd.to_datetime(raw_data.date,infer_datetime_format=True)
    last_day=raw_data['day'].iloc[0]
    one_month_prior=last_day - pd.Timedelta('30D')
    latest_data=raw_data[raw_data['day']>=one_month_prior] #this dataframe contains only the last month of data

    p = figure(x_axis_type="datetime", title=app_tickers.code+" Value in "+str(last_day.year), plot_height=350, plot_width=800)
    #x_axis_type='datetime' tells bokeh that we will have time data on the x axis
    p.xgrid.grid_line_color=None
    p.ygrid.grid_line_alpha=0.5
    p.xaxis.axis_label = 'Day'
    p.yaxis.axis_label = 'Value'
    p.xaxis.major_label_orientation = 1.57#np.pi/2
    p.xaxis.ticker = DaysTicker(days=list(range(1,31)))
    p.line(latest_data.day, latest_data.close, color="blue", legend_label="close")
    p.legend.location = "top_left"

    script, div =components(p)

    return render_template('layout_plot.html',script=script,div=div,ticker=app_tickers.code)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app_tickers.run(host='0.0.0.0', port=port, debug=True)
#if __name__ == '__main__':
 #   app_tickers.run(debug=True)