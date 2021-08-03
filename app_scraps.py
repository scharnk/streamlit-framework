old app.py

import streamlit as st
import numpy as np
import pandas as pd
# import base64
# import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
# from dotenv import dotenv_values
from alpha_vantage.timeseries import TimeSeries
import pandas_bokeh
from bokeh.plotting import figure, show

################################ GET DATA ######################################

project_folder = os.path.expanduser('~/code/GitHub/streamlit-framework')
load_dotenv(os.path.join(project_folder,'.env'))
key = os.getenv("API_KEY")
ts = TimeSeries(key, output_format='pandas')

############################### STREAMLIT ######################################
header = st.beta_container()
dataset = st.beta_container()
features = st.beta_container()

with header:
    st.title('Stock Ticker Milestone Project')
    st.text('Stock data acquired via the Alpha Vantage API')
    st.text('App deployed using Heroku')
test = st.sidebar.beta_container()
with test:
    st.title('Select Features')
    # st.selectbox('Stock Ticker Name?', options = ['AARP','AMZN','MSFT','GOOG'])
    # st.selectbox('Year?', options = ['2015','2016','2017','2018','2019','2020'])
    # st.selectbox('Month?', options = ['January','February','March','April','May','June','July','August','September','October','November','December'])
    st.text("Type the name of a stock ticker")
    ticker = st.text_input("(i.e. 'AARP', 'AMZN', 'MSFT', 'GOOG', etc.)", 'GOOG')
    # st.number_input("Days", min_value = 1, max_value = 365, value=1, step=1)
    display1 = ('January','February','March','April','May','June','July','August','September','October','November','December')
    display2 = ['2015','2016','2017','2018','2019','2020']
    display3 = list(range(1,32))
    options1 = list(range(len(display1)))
    options2 = range(len(display2))
    options3 = range(1,len(display3))

    data, meta = ts.get_intraday(ticker, interval='60min', outputsize='full')
    # data, meta = ts.get_daily_adjusted('TSLA')

    month = st.selectbox('MONTH:', options1, format_func=lambda x: display1[x])
    month = month+1
    day_start = st.selectbox('START DAY:', options3, format_func=lambda x: x)
    year = st.selectbox('START YEAR:', options2, format_func=lambda x: display2[x])

    month2 = st.selectbox('END MONTH:', options1, format_func=lambda x: display1[x])
    month2 = month+1
    day_end = st.selectbox('START YEAR:', options3, format_func=lambda x: x)
    year2 = st.selectbox('END YEAR:', options2, format_func=lambda x: display2[x])


    cols = ['open','high','low','close','volume']
    data.columns = cols
    data['day'] = data.index.date
    data['time'] = data.index.time
    #filter data by YEAR
    #filter data by month?

    US_daily_market = data.between_time('09:30:00','16:00:00').groupby('day').agg({'low':min, 'high':max}).sort_index()


# df = df[df['Date'].dt.month == 11]
# Same works for days or years, where you can substitute dt.month with dt.day or dt.year

    # data.loc['2021-01-01']
    # aapl, meta = ts.get_daily(symbol = 'AAPL')
    # print(aapl['2019-09-12'])




    #
    # after_start_date = US_daily_market["day"] >= start_date
    # before_end_date = US_daily_market["day"] <= end_date
    # between_two_dates = after_start_date & before_end_date
    # US_daily_market = US_daily_market.loc[between_two_dates]

    # df['YEAR'] = df.index.year
    # df['MONTH'] = df.index.month
    # st.write(type(US_daily_market['day']))

# # Convert the date to datetime64
    US_daily_market = US_daily_market.reset_index()
    US_daily_market['date'] = pd.to_datetime(US_daily_market['day'], format='%Y-%m-%d')
#
# # Filter data between two dates
# filtered_df = df.query("date >= '2020-08-01' \
#                        and date < '2020-09-01'")
    # df['day']=pd.to_datetime(df['day'],)
    # US_daily_market = US_daily_market[US_daily_market[]

    # df = df[df['day'].dt.year == 2020]
     # & df['day'].dt.month == str(month)]
    # US_daily_market = US_daily_market.reset_index()
    US_daily_market = US_daily_market[(US_daily_market['date'].dt.year == 2020) & (US_daily_market['date'].dt.month == 4)]

    US_daily_market = US_daily_market.reset_index()
    start_date = (str(year) + '-' + str(month) + '-' + str(day_start))
        # # "2019-1-1"
    end_date = (str(year2) + '-' + str(month2) + '-' + str(day_end))
#         filtered_df =df.loc[df["Joined_date"].between('2019-06-1', '2020-02-05')]
# print(filtered_df)
    US_daily_market = US_daily_market.loc[start_date:end_date]
    # filtered_df=df.loc['2019-06-1':'2020-02-05']
    date = US_daily_market['date']
    x = US_daily_market['low']
    y = US_daily_market['high']

    # st.write(month)

# display = ("male", "female")
# options = list(range(len(display)))
# value = st.selectbox("gender", options, format_func=lambda x: display[x])
# st.write(value)

# data = [['Le goumet', 10], ['The Alcove', 15], ['Mojo Restaurant', 14], ['Mojo Restaurant', 1]]
#
# # Create the pandas DataFrame
# df = pd.DataFrame(data, columns=['Name', 'ID'])
#
# values = df['Name'].tolist()
# options = df['ID'].tolist()
# dic = dict(zip(options, values))
#
# a = st.sidebar.selectbox('Choose a restaurant', options, format_func=lambda x: dic[x])

    # st.sidebar.slider('How many days to look at?', min_value = 1, max_value = 30, value=1, step=1)

with dataset:
    st.header("Stock Market Data For: '{}'".format(ticker))
    st.text('Data visualization constructed with Bokeh, from hourly intraday stock data')
    # st.bar_chart()
    g1_col, g2_col = st.beta_columns(2)
    # days = g1_col.selectbox('Which companies to examine?', options = ['AARP','AMZN','MSFT','GOOG'])
    # days = g2_col.slider('How many days to look at?', min_value = 1, max_value = 30, value=1, step=1)
    # US_market.loc[US_market.groupby('day')['low'].idxmin()]

    p = figure(title="The Highs and Lows of: '{}'".format(ticker), x_axis_type='datetime', x_axis_label='Date', y_axis_label='Value (USD)')
    p.line(date, y, legend_label="Max/day (USD)", line_width=2)
    p.line(date, x, color= "red", legend_label="Min/day (USD)", line_width=2)
    # show(p)
    st.bokeh_chart(p, use_container_width=True)

################################## BOKEH #######################################

################################################################################
# useful links:
#
# bokeh:
#   https://www.youtube.com/watch?v=tnOgrlqA0Bc
#   https://pythonforundergradengineers.com/streamlit-app-with-bokeh.html
# alpha vantage:
#   https://www.youtube.com/watch?v=WJ2t_LYb__0
# streamlit:
#   four part series, used first three:
#   https://www.youtube.com/watch?v=CSv2TBA9_2E
