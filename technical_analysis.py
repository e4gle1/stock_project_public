from database import returnCloses, updateDBDocument, returnVolume
from ta import *
from ta.volatility import BollingerBands
from ta.trend import SMAIndicator
import requests
import traceback
import json
import pandas as pd
import asyncio
from webhook import webhookDiscord, webhookDiscordHV, webhookDiscordTechnical
loop = asyncio.get_event_loop()


def historical(ticker):
    r = requests.get(
        f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/minute/2021-03-26/2021-03-26?unadjusted=true&sort=desc&limit=20&apiKey=#######')
    data = r.json()
    arr = []
    for candle in data['results']:
        candle = candle['c']
        arr.append(candle)
    df = pd.DataFrame(arr, columns=['close'])
    print(df['close'][19])
    return df


def PT(price):
    entry = price
    stop_loss = round(abs((price*0.08)-price), 3)
    profit = round(abs((price*0.035)+price), 3)
    return stop_loss, profit


async def checkTechnical(ticker, volume):
    try:
        closes, closesARR = await returnCloses(ticker)
        # volumeARR = await returnVolume(ticker)

        def upperBollingerBand(ticker, volume):
            if len(closesARR) == 20:
                indicator_bb = BollingerBands(
                    close=closes['close'], window=20, window_dev=2, fillna=False)
                upBB = indicator_bb.bollinger_hband()[19]
                last = closes['close'][19]
                if last > upBB:
                    stop_loss, profit = PT(last)
                    if volume > 150000:
                        webhookDiscordHV(ticker, last, stop_loss, profit, volume)
                        return
                    webhookDiscord(ticker)

        def crossingSMA(ticker):
            sma20 = sum(closesARR)/20
            if closes['close'][18] < sma20 and closes['close'][19] > sma20:
                webhookDiscordTechnical(
                    ticker, 'SMA20CROSS', closes['close'][19], volume)

        def plus20(n):
            plus_20 = (abs((n*(1+0.2))))
            return plus_20
        # plus_20 = plus_20(volumeARR[18])
        # def unusalVolume():
        #     volume = volumeARR[19]
        #     plus_20 = plus_20(volumeARR[18])
        #     print(plus_20, volume)
        #     if volume >= plus_20:
        #         webhookDiscordTechnical(
        #             ticker, 'VOLUME INCREASE', closes['close'][19], volume)
        # try:
        #     unusalVolume()
        # except Exception as e:
        #     traceback.print_exc()
        upperBollingerBand(ticker, volume)
        crossingSMA(ticker)
    except Exception as e:
        print(e)