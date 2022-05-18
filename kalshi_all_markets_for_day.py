# https://kalshi.com/market-data

# Import modules
import json
import requests
import pandas as pd
import numpy as np
import datetime

# Pull in one day of market data from https://kalshi.com/market-data
# Change date in URL as needed
URL = "https://kalshi-public-docs.s3.amazonaws.com/reporting/market_data_2022-05-15.json"
response = requests.get(URL)
jsondata = response.json()
data = json.dumps(jsondata)

# Convert JSON to dataframe
df = pd.DataFrame(eval(data))

# Write dataframe to CSV file in working directory
df.to_csv(r'./kalshi_all_markets_for_day.csv', sep=',', encoding='utf-8', header='true')