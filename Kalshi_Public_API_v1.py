# API Documentation: https://kalshi-public-docs.s3.amazonaws.com/KalshiAPI.html

# Import modules
import json
import requests
import pandas as pd
from datetime import date
from KalshiClientsBase import ExchangeClient # KalshiClientsBase.py from KalshiAPIStarterCode.zip

# Credentials
username = "" # change this 
password = "" # change this (for extra security, Kalshi recommends using a config file)
exchange_api_base = "https://trading-api.kalshi.com"

# Log in
exchange_client = ExchangeClient(exchange_api_base, username, password)

# Get public market data
jsondata = exchange_client.get_public_markets()

# Add JSON data to a list
data = []
for p in jsondata['markets']:
	for k in p['settlement_sources']:
			data.append([p['id'],p['title'],p['category'],p['tags'],p['ranged_group_name'],p['image_url'],p['min_tick_size'],p['settle_details'],k['url'],k['name'],p['ticker_name'],p['create_date'],p['list_date'],p['open_date'],p['close_date'],p['expiration_date'],p['status'],p['expiration_value'],p['description_context'],p['description_case_yes'],p['description_case_no'],p['yes_bid'],p['yes_ask'],p['last_price'],p['previous_yes_bid'],p['previous_yes_ask'],p['previous_price'],p['volume'],p['recent_volume'],p['open_interest'],p['liquidity'],p['dollar_volume'],p['dollar_recent_volume'],p['dollar_open_interest'],p['result'],p['underlying'],p['ranged_group_ticker'],p['frequency_in_days'],p['metrics_tags'],p['mini_title'],p['sub_title'],p['can_close_early'],p['original_expiration_date'],p['rulebook_variables']])

# Convert list to dataframe
df = pd.DataFrame(data)

# Add column names
df.columns=['id','title','category','tags','ranged_group_name','image_url','min_tick_size','settle_details','settlement_sources_url','settlement_sources_name','ticker_name','create_date','list_date','open_date','close_date','expiration_date','status','expiration_value','description_context','description_case_yes','description_case_no','yes_bid','yes_ask','last_price','previous_yes_bid','previous_yes_ask','previous_price','volume','recent_volume','open_interest','liquidity','dollar_volume','dollar_recent_volume','dollar_open_interest','result','underlying','ranged_group_ticker','frequency_in_days','metrics_tags','mini_title','sub_title','can_close_early','original_expiration_date','rulebook_variables']

# Write to local directory
today = date.today()
df.to_csv(r'./kalshi_API_public_markets_'+ str(today) +'.csv', sep=',', encoding='utf-8', header='true')
