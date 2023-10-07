from datetime import timedelta
import pandas as pd

def printdelta(start, end):
    print(timedelta(seconds=end-start))

def loadData(file:str):
    df = pd.read_csv(file, delim_whitespace=True, header=0)
    return df

def sliceDf(index, constant, df):
    return df[index:constant+index]

