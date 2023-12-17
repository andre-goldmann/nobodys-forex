import math
import pandas as pd
import pandas_ta as ta

def tThree(df, Length=5):
    df['xe1'] = ta.ema(df['close'], length=Length)
    df['xe2'] = ta.ema(df['xe1'], length=Length)
    df['xe3'] = ta.ema(df['xe2'], length=Length)
    df['xe4'] = ta.ema(df['xe3'], length=Length)
    df['xe5'] = ta.ema(df['xe4'], length=Length)
    df['xe6'] = ta.ema(df['xe5'], length=Length)

    b = 0.7
    c1 = -b*b*b
    c2 = 3*b*b+3*b*b*b
    c3 = -6*b*b-3*b-3*b*b*b
    c4 = 1+3*b+b*b*b+3*b*b
    df['nT3Average'] = c1 * df['xe6'] + c2 * df['xe5'] + c3 * df['xe4'] + c4 * df['xe3']


def f_LazyLine(_data, _length):
    w1 = 0
    w2 = 0
    w3 = 0
    L1 = 0.0
    L2 = 0.0
    L3 = 0.0
    w = _length / 3

    if _length > 2:
        w2 = round(w)
        w1 = round((_length - w2) / 2)
        w3 = int((_length - w2) / 2)

        L1 = pd.Series(_data).rolling(window=w1, min_periods=1).mean().values
        L2 = pd.Series(L1).rolling(window=w2, min_periods=1).mean().values
        L3 = pd.Series(L2).rolling(window=w3, min_periods=1).mean().values[-1]

        return L3
    else:
        L3 = _data
        return L3

if __name__ == "__main__":
    # Example usage:
    _data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    _length = 9
    result = f_LazyLine(_data, _length)
    #print(result)
    data = {'Date': pd.date_range(start='2022-01-01', periods=10),
            'Value': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}

    df = pd.DataFrame(data)

    # Select the entry immediately preceding the last entry
    previous_to_last_entry = df['Value'].iloc[len(df)-5:len(df)-1]#df.tail(1).tail(2)#df.iloc[-2].tail(8)
    print(previous_to_last_entry)
