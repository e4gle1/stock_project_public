from prime_DB import importTickers
import pprint
import requests
import traceback
import json
import asyncio
import pymongo
from polygon import RESTClient
DATABASE_NAME = 'stockalerts'
COLLECTION_NAME = 'stockdata'
DATABASE_URL = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=false'
client = pymongo.MongoClient(DATABASE_URL)
database = client[DATABASE_NAME]
collection = database[COLLECTION_NAME]


tickers = importTickers()


async def historical(ticker):
    try:
        r = requests.get(
            f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/minute/2021-04-01/2021-04-01?unadjusted=true&sort=desc&limit=20&apiKey=##########').json()
        arr = []
        for candle in r['results']:
            candle = candle['c']
            arr.append(candle)
        return arr
    except Exception as e:
        traceback.print_exc()


def updateDBDocument(ticker, open, low, close, high):
    search = {'ticker': ticker}
    values = {'$push': {'candles': {'open': open, 'low': low, 'close': close,
                                    'high': high}}}
    collection.update_one(search, values)
    print('UPDATED')


async def populate():
    try:
        tickers = importTickers()
        for ticker in tickers:
            candles = await historical(ticker)
            try:
                for i in reversed(range(20)):
                    updateDBDocument(ticker, 0, 0, candles[i], 0)
            except Exception as e:
                traceback.print_exc()
    except Exception as e:
        traceback.print_exc()
asyncio.run(populate())
