# https://kalshi.com/market-data

# Import modules
import json
import requests
import pandas as pd
import numpy as np
import datetime
from datetime import date, timedelta

# Set dates
daybefore = date.today() - timedelta(days=1)
daybefore.strftime('%m%d%y')
start_date = pd.to_datetime('2021-06-30')
daterange = pd.date_range(start_date, daybefore).strftime('%Y-%m-%d').tolist()

# Create list of dataframes
list_of_dataframes = []

# Loop through list of dates
for i in daterange:

	# Pull in market data 
	base_url = "https://kalshi-public-docs.s3.amazonaws.com/reporting/market_data_"
	end_url = ".json"
	URL = base_url + str(i) + end_url
	response = requests.get(URL)
	jsondata = response.json()
	data = json.dumps(jsondata)

	# Convert JSON to dataframe
	df = pd.DataFrame(eval(data))
	
	# Append to list of dataframes
	list_of_dataframes.append(df)

# Concatenate list of dataframes into df_all
df_all = pd.concat(list_of_dataframes)

# Reset index
df_all.reset_index(level=0, inplace=True, drop=True)

# Write out to local directory
df_all.to_csv(r'./kalshi_all_markets_'+ str(daybefore) +'.csv', sep=',', encoding='utf-8', header='true')