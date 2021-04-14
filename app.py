import streamlit as st
import pandas as pd
# import base64
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv
# from dotenv import dotenv_values
from alpha_vantage.timeseries import TimeSeries
import os
import pandas_bokeh

################################ GET DATA ######################################

project_folder = os.path.expanduser('~/code/GitHub/streamlit-framework')
load_dotenv(os.path.join(project_folder,'.env'))

key = os.getenv("API_KEY")

ts = TimeSeries(key, output_format='pandas')
data, meta = ts.get_intraday('TSLA', interval='5min', outputsize='full')

cols = ['open','high','low','close','volume']
data.columns = cols
data['day'] = data.index.date
data['time'] = data.index.time

US_market = data.between_time('09:30:00','16:00:00').groupby('day').agg({'low':min, 'high':max}).sort_index()

# data.loc['2021-01-01']
# aapl, meta = ts.get_daily(symbol = 'AAPL')
# print(aapl['2019-09-12'])

################################## BOKEH #######################################

# from bokeh.plotting import figure, output_file, show

# output_file("patch.html")

# p = figure(plot_width=400, plot_height=400)

# p.multi_line([[1, 3, 2], [3, 4, 6, 6]], [[2, 1, 4], [4, 7, 8, 5]],
#              color=["firebrick", "navy"], alpha=[0.8, 0.3], line_width=4)
#
# show(p)





############################### STREAMLIT ######################################
header = st.beta_container()
dataset = st.beta_container()
features = st.beta_container()

with header:
    st.title('Stock Ticker Milestone Project')
    st.text('Stock data acquired from the Alpha Vantage API')

test = st.sidebar.beta_container()
with test:
    st.title('Select Features')
    st.selectbox('Stock Ticker Name?', options = ['AARP','AMZN','MSFT','GOOG'])
    st.selectbox('Year?', options = ['2015','2016','2017','2018','2019','2020'])
    st.selectbox('Month?', options = ['January','February','March','April','May','June','July','August','September','October','November','December'])
    # st.sidebar.slider('How many days to look at?', min_value = 1, max_value = 30, value=1, step=1)

with dataset:
    st.header('Stock Market Data')
    # st.bar_chart()
    g1_col, g2_col = st.beta_columns(2)
    # days = g1_col.selectbox('Which companies to examine?', options = ['AARP','AMZN','MSFT','GOOG'])
    # days = g2_col.slider('How many days to look at?', min_value = 1, max_value = 30, value=1, step=1)
    # US_market.loc[US_market.groupby('day')['low'].idxmin()]
    US_market.reset_index()
    from bokeh.plotting import figure, show
    # x = [1, 2, 3, 4, 5]
    # y = [6, 7, 2, 4, 5]
    x = US_market['low']
    y = US_market['high']
    p = figure(title="Simple line example", x_axis_type='datetime', x_axis_label='x', y_axis_label='y')
    p.line(x, y, legend_label="Temp.", line_width=2)
    show(p)

    # US_market.plot_bokeh(kind='line', x = 'low', y = 'high')

################################################################################
# useful links:
#
# bokeh:
#   https://www.youtube.com/watch?v=tnOgrlqA0Bc
# alpha vantage:
#   https://www.youtube.com/watch?v=WJ2t_LYb__0
# streamlit:
#   four part series, used first three:
#   https://www.youtube.com/watch?v=CSv2TBA9_2E
