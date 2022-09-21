import ccxt
import pandas as pd
from datetime import datetime
import time
import threading
import ta

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', True)

exchange_binance = ccxt.binance()

# binance.timeframes
# {'1m': '1m', '3m': '3m', '5m': '5m', '15m': '15m', '30m': '30m', '1h': '1h', '2h': '2h', '4h': '4h', '6h': '6h', '8h': '8h', '12h': '12h',
#  '1d': '1d', '3d': '3d', '1w': '1w', '1M': '1M'}
# exchange.set_sandbox_mode(True)

markets = exchange_binance.fetch_markets()

# print(markets)
for oneline in markets:
    symbol = oneline['id']
    if symbol == 'BTCUSDT':
        result = exchange_binance.fetch_ohlcv(symbol, '15m', limit=1000)
        # print(symbol, result)
        dframe = pd.DataFrame(result)
        # print(dframe[0])  # UTC timestamp in milliseconds, integer
        # print(dframe[1])
        # print(dframe[2])
        # print(dframe[3])
        # print(dframe[4])

        dframe['timestamp'] = pd.to_numeric(dframe[0])
        dframe['open'] = pd.to_numeric(dframe[1])
        dframe['high'] = pd.to_numeric(dframe[2])
        dframe['low'] = pd.to_numeric(dframe[3])
        dframe['close'] = pd.to_numeric(dframe[4])

        dframe['ICH_SSB'] = ta.trend.ichimoku_b(dframe['high'], dframe['low'], window2=26, window3=52).shift(26)
        # print(dframe['ICH_SSB'])

        dframe['ICH_SSA'] = ta.trend.ichimoku_a(dframe['high'], dframe['low'], window1=9, window2=26).shift(26)
        # print(dframe['ICH_SSA'])

        dframe['ICH_KS'] = ta.trend.ichimoku_base_line(dframe['high'], dframe['low'])
        # print(dframe['ICH_KS'])

        dframe['ICH_TS'] = ta.trend.ichimoku_conversion_line(dframe['high'], dframe['low'])
        # print(dframe['ICH_TS'])

        dframe['ICH_CS'] = dframe['close'].shift(-26)
        # print(dframe['ICH_CS'])

        # print("SSB", dframe['ICH_SSB'].iloc[-1])  # SSB at the current price
        # print("SSA", dframe['ICH_SSA'].iloc[-1])  # SSB at the current price
        # print("KS", dframe['ICH_KS'].iloc[-1])  # SSB at the current price
        # print("TS", dframe['ICH_TS'].iloc[-1])  # SSB at the current price
        # print("CS", dframe['ICH_CS'].iloc[-27])  # SSB at the current price

        price_open = dframe['open'].iloc[-1]
        price_high = dframe['high'].iloc[-1]
        price_low = dframe['low'].iloc[-1]
        price_close = dframe['close'].iloc[-1]
        # print("price_open", price_open)
        # print("price_high", price_high)
        # print("price_low", price_low)
        # print("price_close", price_close)

        price_open_chikou = dframe['open'].iloc[-27]
        price_high_chikou = dframe['high'].iloc[-27]
        price_low_chikou = dframe['low'].iloc[-27]
        price_close_chikou = dframe['close'].iloc[-27]
        # print("price_open_chikou", price_open_chikou)
        # print("price_high_chikou", price_high_chikou)
        # print("price_low_chikou", price_low_chikou)
        # print("price_close_chikou", price_close_chikou)

        tenkan_chikou = dframe['ICH_TS'].iloc[-27]
        kijun_chikou = dframe['ICH_KS'].iloc[-27]
        print("tenkan_chikou", tenkan_chikou)
        print("kijun_chikou", kijun_chikou)
        
