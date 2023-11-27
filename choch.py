import pandas as pd
import numpy as np
import pandas_ta as ta
from scipy import stats


# Importing the dataset using method "loadDfFromDb" from DataBaseManagement
from DataBaseManagement import loadDfFromDb, TimeFrame
#  using symbol 'EURUSD' and timeframe TimeFrame.PERIOD_H4
df = loadDfFromDb('EURUSD', TimeFrame.PERIOD_H4)
# remove where volume is 0
df = df[df['volume'] != 0]
# Calculate the True Range
df['tr'] = ta.true_range(df['high'], df['low'], df['close'])
# Calculate the ATR
df['atr'] = ta.atr(df['high'], df['low'], df['close'])
# reset index
df = df.reset_index(drop=True, inplace=False)
# calculate rsi with period 12
df['rsi'] = ta.rsi(df['close'], length=12)
# calculate ema with period 150
df['ema'] = ta.ema(df['close'], length=150)
# select first 500 rows
df = df.iloc[:500]

EMASignal = [0]*len(df)
backCandles = 15
# iterate over df using backCandles
for row in range(backCandles, len(df)):
    upt = 1
    dnt = 1
    # iterate over df using backCandles
    for i in range(row - backCandles, row+1):
        # if max of open and close greater than or equal to ema then dnt = 0
        if max(df['open'][i], df['close'][i]) >= df['ema'][i]:
            dnt = 0
        # if max of open and close smaller than or equal to ema then upt = 0
        if min(df['open'][i], df['close'][i]) <= df['ema'][i]:
            upt = 0

    # if upt is 1 and dnt is 1 then EMASignal is 3
    if upt == 1 and dnt == 1:
        EMASignal[row] = 3
    # else if upt is 1 then EMASignal is 2
    elif upt == 1:
        EMASignal[row] = 2
    # else if dnt is 1 then EMASignal is 1
    elif dnt == 1:
        EMASignal[row] = 1

    # store EMASignal in df
    df['EMASignal'] = EMASignal

def isPivot(candle, window):
    """
    function that dectects if a candle is a pivot or not
    """
    # if candle is the max or min of the window then return True
    if candle -window < 0 or candle + window >= len(df):
        return 0
    pivotHigh = 1
    pivotLow = 2
    # iterate over the window
    for i in range(candle-window, candle+window+1):
        if df.iloc[candle]['high'] < df.iloc[i]['high']:
            pivotHigh = 0
        if df.iloc[candle]['low'] > df.iloc[i]['low']:
            pivotLow = 0
    if (pivotHigh and pivotLow):
        return 3
    elif pivotHigh:
        return pivotHigh
    elif pivotLow:
        return pivotLow
    else:
        return 0