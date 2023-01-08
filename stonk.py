import yfinance as yf

def get_response(message: str) -> str:
    lower = message.lower()
    kys = 'kys'
    ticker = yf.Ticker(lower)
    if ticker.info == None:
        return kys
    data = ticker.history()
    quote = data['Close'].iloc[-1]
    return quote