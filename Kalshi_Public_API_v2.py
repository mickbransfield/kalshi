# Original code take from https://github.com/ksyeung/PS-ScrapeKalshi and converted from PowerShell to Python via ChatGPT on August 7, 2023

# API Documentation: https://kalshi-public-docs.s3.amazonaws.com/KalshiAPI.html

# Import modules
import json
import requests
import pandas as pd
import numpy as np
import datetime
import os
import csv
import time

endpoint = "https://trading-api.kalshi.com/trade-api/v2"

def get_bearer_token(email, password):
    url = f"{endpoint}/login"
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    body = {
        "email": "", # insert between ""
        "password": "" # insert between ""
    }
    response = requests.post(url, headers=headers, json=body)
    return f"Bearer {response.json()['token']}"

def get_all_data(category, url, headers, sleep_time_in_milliseconds=105):
    data = []
    cursor = None

    while cursor != "":
        url_with_cursor = f"{url}&cursor={cursor}" if cursor else url
        response = requests.get(url_with_cursor, headers=headers).json()
        cursor = response.get("cursor")

        if category == "markets":
            data.extend(response.get("markets", []))
        elif category == "trades":
            data.extend(response.get("trades", []))
        elif category == "history":
            data.extend(response.get("history", []))
        elif category == "events":
            data.extend(response.get("events", []))
        
        time.sleep(sleep_time_in_milliseconds / 1000)

    return data

def get_all_markets(bearer_token, path):
    url = f"{endpoint}/markets?limit=1000&status=open"
    headers = {
        "accept": "application/json",
        "Authorization": bearer_token
    }

    data = get_all_data("markets", url, headers)
    with open(path, 'a', newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys(), extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data)

def get_all_trades(tickers, path):
    headers = {
        "accept": "application/json"
    }

    for ticker in tickers:
        url = f"{endpoint}/markets/trades?limit=1000&ticker={ticker}"
        trades_data = get_all_data("trades", url, headers)

        with open(path, 'a', newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=trades_data[0].keys(), extrasaction='ignore')
            writer.writeheader()
            writer.writerows(trades_data)

def get_all_markets_history(bearer_token, tickers, path):
    headers = {
        "accept": "application/json",
        "Authorization": bearer_token
    }

    for ticker in tickers:
        url = f"{endpoint}/markets/{ticker}/history?limit=1000"
        data = get_all_data("history", url, headers)

        for row in data:
            row["ticker"] = ticker
        
        with open(path, 'a', newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys(), extrasaction='ignore')
            writer.writeheader()
            writer.writerows(data)

def extract_tickers_from_markets_data(markets_data):
    return [row['ticker'] for row in markets_data]


token = get_bearer_token(email="email", password="password")

snapshotdate = datetime.datetime.today().strftime("%Y-%m-%d %H_%M_%S")

get_all_markets(bearer_token=token, path='Kalshi_Public_API_v2_'+snapshotdate+'.csv')


