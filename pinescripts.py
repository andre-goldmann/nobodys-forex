import math
import pandas as pd
import pandas_ta as ta
import os
import sys
import traceback
from datetime import datetime
from datetime import timedelta
from timeit import default_timer as timer
import uvicorn
import pandas as pd
import statsmodels.api as sm
from dotenv import load_dotenv
from pydantic import BaseModel
from sqlalchemy import Enum, Column, Integer, Float, text
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy import create_engine, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import sessionmaker
import numpy as np
from DataBaseManagement import initTradingDb, TimeFrame, storeData, loadDfFromDb
from utils import loadData
from fastapi import FastAPI, Request, status
from fastapi import WebSocket, WebSocketDisconnect, Form
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

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

@app.get("/linecolor/")
def lineColor():
    print("I was called")
    return "Blue"

if __name__ == "__main__":
    initTradingDb()
    symbol = "EURUSD"
    timeframe = TimeFrame.PERIOD_M15
    #storeData("EURUSD", TimeFrame.PERIOD_M15)
    data = loadDfFromDb(symbol, timeframe, 10000)

    data = data.set_index('DATETIME')
    data = data.dropna()
    #data['Open'] = data.OPEN
    #data['High'] = data.HIGH
    #data['Low'] = data.LOW
    data['close'] = data.CLOSE
    #data['Volume'] = data.TICKVOL

    #for index, row in data.tail(-1).tail(25).iterrows():
    #    process_row(index, row)

    LL = f_LazyLine(data['close'].tail(-1).tail(200), 15)
    LLPrev = f_LazyLine(data['close'].iloc[len(data)-200:len(data)-1], 15)
    data['redkslow'] = data['close'].apply(lambda row: f_LazyLine(row, 15))
    conditions  = [ data['redkslow'] > data['redkslow'].shift(1), data['redkslow'] < data['redkslow'].shift(1), data['redkslow'] == data['redkslow'].shift(1) ]
    choices     = [ "Long", 'Short', 'Ranging' ]
    data['redkslowtrend'] = np.select(conditions, choices)#np.where(, "Long", "Short") # (data['redkslow'] > data['redkslow'].shift(1))  # data.apply(lambda row: trendRedkslow(row))

    tThree(data, 300)
    print(data.tail(-1).tail(15))


    uvicorn.run(app, host="0.0.0.0", port=8000)
