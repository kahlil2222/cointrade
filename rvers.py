import pyupbit
import pandas as pd
import time
import datetime


upbit = pyupbit.Upbit("uJsYNAuY4pPft9xOVTlg51BR11Zvl1MqFTHOPq5g", "cneOmWgxCn5UvfgyLyl4xeRQw3u1aKIAH8MdY1Kt")
symbol = pyupbit.get_tickers("KRW")

while True:
    for value in symbol :
        sym = value[4:len(value)]
   
        candles = pyupbit.get_ohlcv(value, interval="minute5", count=202)
        ticker = pyupbit.get_orderbook(value)["orderbook_units"][0]["ask_price"]
        if candles is not None and not candles.empty:
            avg20 = pd.DataFrame(candles)
            avg20["20d_ma"] = avg20["close"].rolling(window=20).mean()
            close_preavg20 = avg20["20d_ma"].iloc[-2]       
            pre_price = avg20["close"].iloc[-2]
            close_avg20 = avg20["20d_ma"].iloc[-1]
            price = avg20["close"].iloc[-1]
            volume = avg20["volume"].iloc[-1]
            avg20["200ma_vol"] = avg20["volume"].rolling(window=200).mean()
            vol200 = avg20["200ma_vol"].iloc[-2]
            max_price = avg20['close'][-3:-1].max()
            max_pirce = float(max_price)
            premax_price = avg20['close'][-4:-2].max()
            premax_price = float(premax_price)
            try:
                balances = upbit.get_balances()
                cal = pd.DataFrame(balances)
                cal = cal.set_index('currency')
                loc_cal = cal.loc[sym, 'avg_buy_price']
                loc_cal = float(loc_cal)
                loc_krw = cal.loc["KRW", 'balance' ]
                loc_krw = float(loc_krw)
                profit = (ticker - loc_cal) / loc_cal * 100
                balance = cal.loc[sym, 'balance']
                if profit <= -1 or (avg20["close"].iloc[-1] - max_price)/ max_price * 100 <= -1:
                    upbit.sell_market_order(value, balance)
                    print(sym)
                    print("avgbuy_price:", loc_cal)
                    print("profit:", profit)
                if loc_krw >= 6000 and (price - premax_price)/ premax_price *100 >= 1:
                    upbit.buy_market_order(value, 6000)
            except KeyError:
                
                if loc_krw >= 6000 and pre_price < close_preavg20 and price > close_avg20 and volume > vol200 *1.5:
                    upbit.buy_market_order(value, 6000)
                    print(sym)
                    print("20ma prevolume:", avg20["20d_ma"].iloc[-2])
                    print("pre price:", avg20["close"].iloc[-2])
                    print("avr volume :", avg20["200ma_vol"].iloc[-2])
                    print("current volume:", avg20["volume"].iloc[-1])
                    print("20ma volume:", avg20["20d_ma"].iloc[-1] )
                    print("current price:", avg20["close"].iloc[-1])
                    print(f"Bought {6000 / avg20['close'][-2]} {value} at market price.")
    
    print(datetime.datetime.now())
    time.sleep(120)

