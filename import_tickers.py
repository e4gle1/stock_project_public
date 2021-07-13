#IMPORT FOR WEBSOCKET SUBSCRIPTIONS

def importTickers():
    ticker_list = []
    ticker_file = open(r'####', 'r')
    tickers = ticker_file.readlines()
    for ticker in tickers:
        ticker_list.append('\'AM.' + ticker.replace('\n', '\''))
    ticker_list = ','.join(ticker_list) + str('\'')
    return ticker_list
