import math
import pandas as pd

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

def trendRedkslow(row):
    print("##########trendRedkslow##################")
    print(row)
    actualValue = row['redkslow']
    previousValue = row['redkslow'].shift(1)
    if actualValue > previousValue:
        return "long"
    elif actualValue < previousValue:
        return "short"
    elif actualValue == previousValue:
        return "ranging"

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
