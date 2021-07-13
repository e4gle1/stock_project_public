import time
import pymongo
import traceback
import pandas as pd
import asyncio
from prime_DB import importTickers
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
db = client['stockalerts']
collection = db['stockdata']
loop = asyncio.get_event_loop()
tickers = importTickers()

async def updateDBDocument(ticker, open, low, close, high, volume):
    try:
        data = await collection.find_one({'ticker': ticker})
        length = len(data['candles'])
        if length < 20:
            await collection.update_one({'ticker': ticker}, {'$push': {'candles': {'open': open, 'low': low, 'close': close,
                                                                                'high': high, 'vol':volume}}})
        if length == 20:
            await collection.update_one({'ticker': ticker}, {'$pop': {'candles': -1}})
            await collection.update_one({'ticker': ticker}, {'$push': {'candles': {'open': open, 'low': low, 'close': close,
                                                                                'high': high, 'vol':volume}}})
    except Exception as e:
        traceback.print_exc()
async def returnCloses(ticker):
    data = await collection.find_one({'ticker': ticker})
    candles = data['candles']
    closes = []
    closesARR = []
    for candle in candles:
        closes.append(candle['close'])
        closesARR.append(candle['close'])
    closes = pd.DataFrame(closes, columns=['close'])
    return closes, closesARR

async def returnVolume(ticker):
    data = await collection.find_one({'ticker': ticker})
    candles = data['candles']
    volume = []
    for vol in candles:
        volume.append(vol['vol'])
    return volume