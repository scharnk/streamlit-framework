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

data, meta = ts.get_intraday('TSLA', interval='60min', outputsize='full')
# data, meta = ts.get_daily_adjusted('TSLA', interval='60min', outputsize='full')

cols = ['open','high','low','close','volume']
data.columns = cols
data['day'] = data.index.date
data['time'] = data.index.time

US_daily_market = data.between_time('09:30:00','16:00:00').groupby('day').agg({'low':min, 'high':max}).sort_index()

# data.loc['2021-01-01']
# aapl, meta = ts.get_daily(symbol = 'AAPL')
# print(aapl['2019-09-12'])

US_daily_market = US_daily_market.reset_index()

day = US_daily_market['day']
x = US_daily_market['low']
y = US_daily_market['high']

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
    st.number_input("Days", min_value = 1, max_value = 365, value=1, step=1)
    options = df[''].tolist()
    st.selectbox('', )

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
    st.text('Data visualization constructed with Bokeh')
    # st.bar_chart()
    g1_col, g2_col = st.beta_columns(2)
    # days = g1_col.selectbox('Which companies to examine?', options = ['AARP','AMZN','MSFT','GOOG'])
    # days = g2_col.slider('How many days to look at?', min_value = 1, max_value = 30, value=1, step=1)
    # US_market.loc[US_market.groupby('day')['low'].idxmin()]

    p = figure(title="The Highs and Lows of: '{}'".format(ticker), x_axis_type='datetime', x_axis_label='Date', y_axis_label='Value (USD)')
    p.line(day, y, legend_label="Max/day (USD)", line_width=2)
    p.line(day, x, color= "red", legend_label="Min/day (USD)", line_width=2)
    # show(p)
    st.bokeh_chart(p, use_container_width=True)

################################## BOKEH #######################################

# import numpy as np
# import streamlit as st
# from bokeh.plotting import figure
# from user_funcs import mohr_c, c_array, X_Y
#
# st.title("Mohr's Circle App")
#
# stress_x = st.sidebar.number_input("stress in x", value=2.0, step=0.1)
# stress_y = st.sidebar.number_input("stress in y", value=5.0, step=0.1)
# shear = st.sidebar.number_input("shear xy", value=4.0, step=0.1)
#
# # find center and radius
# C, R = mohr_c(stress_x, stress_y, shear)
#
# # build arrays plot circle
# circle_x, circle_y = c_array(C, R)
#
# # build arrays to plot line through the circle
# X, Y = X_Y(stress_x, stress_y, shear)
#
# st.sidebar.markdown(f"max stress = {round(C+R,2)}")
# st.sidebar.markdown(f"min stress = {round(C-R,2)}")
# st.sidebar.markdown(f"max shear = {round(R,2)}")
#
# p = figure(
#     title="Mohr's Circle",
#     x_axis_label="stress",
#     y_axis_label="shear",
#     match_aspect=True,
#     tools="pan,reset,save,wheel_zoom",
# )
#
# p.line(circle_x, circle_y, color="#1f77b4", line_width=3, line_alpha=0.6)
# p.line(X, Y, color="#ff7f0e", line_width=3, line_alpha=0.6)
#
# p.xaxis.fixed_location = 0
# p.yaxis.fixed_location = 0
#
# st.bokeh_chart(p)

    # p = figure(title="Simple line example", x_axis_type='datetime', x_axis_label='date', y_axis_label='y')
    # p.scatter(date, y)
    # show(p)

    # output_file("patch.html")

    # p = figure(plot_width=400, plot_height=400)

    # p.multi_line([[1, 3, 2], [3, 4, 6, 6]], [[2, 1, 4], [4, 7, 8, 5]],
    #              color=["firebrick", "navy"], alpha=[0.8, 0.3], line_width=4)

    # US_market.plot_bokeh(kind='line', x = 'low', y = 'high')

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
