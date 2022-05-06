import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from alpha_vantage.timeseries import TimeSeries
import pandas_bokeh
from bokeh.plotting import figure, show, curdoc


################################ GET DATA ######################################

# for local deployment
# project_folder = os.path.expanduser('~/code/GitHub/streamlit-framework')
# load_dotenv(os.path.join(project_folder,'.env'))
# key = os.getenv("API_KEY")
# ts = TimeSeries(key, output_format='pandas')

# for streamlit sharing deployment
key = st.secrets["API_KEY"]

# CHECK FOR ENV VARIABLE BEING SET:
# st.write(
#     "Has environment variable been set?:",
#     os.environ["API_KEY"] == st.secrets["API_KEY"])

ts = TimeSeries(key, output_format='pandas')

# streamlit secrets management url:
# https://www.notion.so/Secrets-Management-730c82af2fc048d383d668c4049fb9bf

############################### STREAMLIT ######################################
header = st.container()
dataset = st.container()
# features = st.container()
test = st.sidebar.container()

# st.markdown("""
# <style>
# .big-font {
#     font-size:300px !important;
# }
# </style>
# """, unsafe_allow_html=True)

# st.markdown('<p class="big-font">Hello World !!</p>', unsafe_allow_html=True)

with header:
    st.title('Stock Ticker Milestone Project')
    st.subheader('Stock data acquired via the Alpha Vantage API')
    st.text('App was originally deployed using Heroku, now solely on Streamlit')    

with test:
    st.title('Select Features')
    st.text("Type the name of a stock ticker")
    ticker = st.text_input("(i.e. 'AARP', 'AMZN', 'MSFT', 'GOOG', etc.)", 'GOOG')
#     data, meta = ts.get_daily_adjusted(ticker, outputsize='full')
#   daily_adjusted has been turned into a premium product since writing this code
    data, meta = ts.get_daily(ticker, outputsize='full')

    display1 = ('January','February','March','April','May','June','July','August','September','October','November','December')
    options1 = list(range(len(display1)))
    YEAR = st.selectbox('YEAR:', ['2021','2020','2019','2018','2017','2016','2015'])
    monthh = st.selectbox('MONTH:', options1, format_func=lambda x: display1[x])
    MONTH = monthh+1

#     cols = ['open','high','low','close','adj_close','volume','divedend','split_coeff']
    cols = ['open','high','low','close','volume']
    data.columns = cols
    data['day'] = data.index.date
    data['time'] = data.index.time

    US_daily_market = data
    US_daily_market.index = pd.to_datetime(US_daily_market.index, format='%Y-%m-%d')

    US_daily_market['month'] = US_daily_market.index.month
    US_daily_market['year'] = US_daily_market.index.year
    US_daily_market = US_daily_market.reset_index()
    US_daily_market = US_daily_market.loc[(US_daily_market['month'] == int(MONTH)) & (US_daily_market['year'] == int(YEAR))]

    date = US_daily_market['day']
    x = US_daily_market['low']
    y = US_daily_market['high']

#     st.empty()
    st.write("#")
    
with dataset:
    st.header("Stock Market Data for '{}' in {}".format(ticker, YEAR))
    st.text('Data visualization constructed with Bokeh, from hourly intraday stock data')
    st.write("##")
    
 
    p = figure(title="The Highs and Lows of '{}' in {}".format(ticker, YEAR), x_axis_type='datetime', x_axis_label='Date (month/day)', y_axis_label='Value (USD)')

    p.line(date, y, legend_label="Max / day (USD)", line_width=2)
    p.line(date, x, color= "red", legend_label="Min / day (USD)", line_width=2)
    
    p.title.text_font_size = '22pt'
    p.legend.label_text_font_size = "16pt"
    
    p.xaxis.axis_label_text_font_size = "16pt"
    p.yaxis.axis_label_text_font_size = "16pt"
    p.xaxis.major_label_text_font_size = "14pt"
    p.yaxis.major_label_text_font_size = "14pt"
    
    st.bokeh_chart(p, use_container_width=True)



################################################################################
# useful links:
#
# bokeh:
#   https://www.youtube.com/watch?v=tnOgrlqA0Bc
#   https://pythonforundergradengineers.com/streamlit-app-with-bokeh.html
# alpha vantage:
#   https://www.youtube.com/watch?v=WJ2t_LYb__0
# streamlit:
#   four part series, used first 2/3:
#   https://www.youtube.com/watch?v=CSv2TBA9_2E
