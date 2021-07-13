import pymongo
DATABASE_NAME = 'stockalerts'
COLLECTION_NAME = 'stockdata'
DATABASE_URL = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=false'
client = pymongo.MongoClient(DATABASE_URL)
database = client[DATABASE_NAME]
collection = database[COLLECTION_NAME]


def importTickers():
    ticker_list = []
    ticker_file = open(r'I:####', 'r')
    tickers = ticker_file.readlines()
    for ticker in tickers:
        ticker_list.append(ticker.replace('\n', ''))
    return ticker_list

if __name__ == '__main__':
    ticker_list = importTickers()


def addDBDocument(ticker):
    stock_entry = {
        'ticker': ticker,
        'candles': []
    }
    collection.insert_one(stock_entry)

if __name__ == '__main__':
    list(map(addDBDocument, ticker_list))
