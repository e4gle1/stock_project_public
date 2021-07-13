from polygon import *
import time
import traceback
import json
import asyncio
from database import updateDBDocument
from import_tickers import importTickers
from technical_analysis import checkTechnical
loop = asyncio.get_event_loop()

def handleData(message):
    response_data = json.loads(message)
    for messageM in response_data:
        if messageM['ev'] == 'status':
            print(messageM)
        if messageM['ev'] == 'AM':
            TICKER = messageM['sym']
            OPEN = messageM['op']
            LOW = messageM['l']
            CLOSE = messageM['c']
            HIGH = messageM['h']
            VOLUME = messageM['v']
            TIME = messageM['e']
            # try:
            #     loop.run_until_complete(updateDBDocument(TICKER, OPEN, LOW, CLOSE, HIGH, VOLUME))
            #     loop.run_until_complete(checkTechnical(TICKER, VOLUME))
            # except Exception as e:
            #     traceback.print_exc()
    

def websocket():
    key = '####'
    my_client = WebSocketClient(STOCKS_CLUSTER, key, handleData)
    my_client.run_async()
    my_client.subscribe(importTickers())

if __name__ == '__main__':
    websocket()
