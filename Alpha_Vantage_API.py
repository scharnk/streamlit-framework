import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv
# from dotenv import dotenv_values
from alpha_vantage.timeseries import TimeSeries

load_dotenv()

require('dotenv').config()
console.log(process.env)

key = process.env.API_KEY
ts = TimeSeries(key)

aapl, meta = ts.get_daily(symbol = 'AAPL')
print(aapl['2019-09-12'])
