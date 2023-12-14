import logging
import datetime
import json
import threading
import time
from datetime import timedelta
from timeit import default_timer as timer
from typing import List

import numpy as np
import pandas as pd
import schedule
import uvicorn
from fastapi import FastAPI, Request, status
from fastapi import WebSocket, WebSocketDisconnect, Form
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
# Bellow the import create a job that will be executed on background
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from scipy.signal import argrelextrema, find_peaks
from sklearn.neighbors import KernelDensity
from typing_extensions import Annotated

from DataBaseManagement import initTradingDb, symbols, storeSignal, Signal, getWaitingSignals, \
    SignalActivationDto, \
    activateSignal, SignalUpdateDto, updateSignalInDb, updateSignalProdInDb, modifySignalInDb, deleteSignalInDb, tradeTypes, \
    getExecutedSignals, HistoryUpdateDto, updateSignalByHistory, getStrategystats, getIgnoredSignals, TimeFrame, \
    getLinesInfo, regressionCalculation, lastCandle, CandlesDto, loadDfFromDb, storeCandleInDb, countEntries, storeData, \
    getSrLevels, SupportResistanceType, storeSupportResistance, SupportResistance, deleteSupportResistance, \
    insertFromFile, countTrades, getInstrumentstats, deleteSignalFromDb, SignalId, deleteIgnoredSignalFromDb, getWaitingSignalsProd
from trendline_breakout import trendline_breakout

#version = f"{sys.version_info.major}.{sys.version_info.minor}"

startDate = "2023-07-01 00:00:00.000000"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

#this is changing, so need to update this
#https://www.iplocation.net/
#app.add_middleware(
#    TrustedHostMiddleware, allowed_hosts=["193.32.248.217"]
#)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

app.add_middleware(CORSMiddleware, allow_origins=["*"])


def receivedMsg(message):
    print(f"{message} received on Queue!!!############")


# Connected svelte: an implement a check list for trades:
# - crossed support/resistance done
# - ema200 crossed ema80 done
# - usw.

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    print(f"Client with id: {client_id} connected!!!")
    last = lastCandle("EURUSD", TimeFrame.PERIOD_M15)
    json_compatible_item_data = jsonable_encoder(last)
    await manager.broadcast(json.dumps(json_compatible_item_data))

    try:
        while True:
            data = await websocket.receive_text()
            #Leave the wait here
            #When a WebSocket connection is closed, the await websocket.receive_text()
            # will raise a WebSocketDisconnect exception, which you can then catch and handle like in this

    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/lastCandle/")
async def getLastCandleStamp(symbol:str, timeFrame:str):
    timeframeEnum: TimeFrame = TimeFrame.__dict__[timeFrame]
    last = lastCandle(symbol, timeframeEnum)
    if last is None:
        return {'stamp': "2016.01.01 00:00:00"}
    return {'stamp': last.DATETIME}


@app.get("/ignoredsignals")
async def ignoredSignals():
    signals = getIgnoredSignals()
    result = []
    #print("###################################")
    #print(f"IgnoredSignals from db loaded:{len(signals)}")
    #print("###################################")
    for signal in signals:
        result.append({'id': signal.id,
                       'json': signal.json,
                       'reason': signal.reason})

    return result

@app.get("/waitingsignalsx")
async def waitingSignals():
    signals = getWaitingSignals()
    result = []
    for signal in signals:
        result.append({'id': signal.id,
                       'symbol': signal.symbol,
                       'type': signal.type,
                       'entry': signal.entry,
                       'sl': signal.sl,
                       'tp': signal.tp,
                       'lots': signal.lots,
                       'stamp': signal.stamp,
                       'strategy': signal.strategy})

    return result

@app.get("/waitingsignalsprod")
async def waitingSignalsProd():
    signals = getWaitingSignalsProd()
    result = []
    for signal in signals:
        result.append({'id': signal.id,
                       'symbol': signal.symbol,
                       'type': signal.type,
                       'entry': signal.entry,
                       'sl': signal.sl,
                       'tp': signal.tp,
                       'lots': signal.lots,
                       'stamp': signal.stamp,
                       'strategy': signal.strategy})

    return result


@app.post("/deletesignal")
async def deleteSignal(id:SignalId):
    deleteSignalFromDb(id)

@app.post("/deleteignoredsignal")
async def deleteIgnoredSignal(id:SignalId):
    deleteIgnoredSignalFromDb(id)


@app.get("/strategystats")
async def strategystats():
    stats = getStrategystats()
    result = []

    for stat in stats:
        if "" != stat.strategy and stat.strategy is not None:
            result.append({'strategy': stat.strategy,
                           'tradestotal': stat.alltrades,
                           'tradesfailed': stat.failedtrades,
                           'tradessuccess': stat.successtrades,
                           'profit': stat.profit,
                           'commission': stat.commission,
                           'swap': stat.swap})

    return result

@app.get("/instrumentstats")
async def instrumentstats(strategy:str):
    stats = getInstrumentstats(strategy)
    result = []

    for stat in stats:
        if "" != stat.symbol and stat.symbol is not None:
            result.append({'symbol': stat.symbol,
                           'tradestotal': stat.alltrades,
                           'tradesfailed': stat.failedtrades,
                           'tradessuccess': stat.successtrades,
                           'profit': stat.profit,
                           'commission': stat.commission,
                           'swap': stat.swap})

    return result

@app.get("/executedsignals")
async def executedSignals(strategy:str):
    signals = getExecutedSignals(strategy)
    result = []
    for signal in signals:
        result.append({'id': signal.id,
                       'symbol': signal.symbol,
                       'type': signal.type,
                       'entry': signal.entry,
                       'sl': signal.sl,
                       'tp': signal.tp,
                       'lots': signal.lots,
                       'stamp': signal.stamp,
                       'strategy': signal.strategy,
                       'activated': signal.activated,
                       'openprice': signal.openprice,
                       'profit': signal.profit,
                       'commision': signal.commision,
                       'swap': signal.swap,
                       'closed': signal.closed,
                       'exit': signal.exit})

    return result

@app.post("/createsignal/")
async def createsignal(symbol: Annotated[str, Form()],
                      type: Annotated[str, Form()],
                      entry: Annotated[float, Form()],
                      sl: Annotated[float, Form()],
                      tp: Annotated[float, Form()],
                      lots: Annotated[float, Form()]):

    if symbol not in symbols:
        print(f"Ignore order because symbol is not handled yet: {symbol}")
        return

    if type not in tradeTypes:
        print(f"Ignore order because type is not handled: {type}")
        return

    storeSignal(Signal(
        symbol=symbol,
        type=type,
        entry=entry,
        sl=sl,
        tp=tp,
        lots=lots
    ))
    return "Order created"

#need to use form here, because delete does not work
@app.post("/deletesignal/")
async def deleteOrder(id: Annotated[int, Form()]):
    deleteSignalInDb(id)
    return "Signal deleted"

@app.post("/modifysignal/")
async def modifySignalIn(id: Annotated[int, Form()],
                      symbol: Annotated[str, Form()],
                      type: Annotated[str, Form()],
                      entry: Annotated[float, Form()],
                      sl: Annotated[float, Form()],
                      tp: Annotated[float, Form()],
                      lots: Annotated[float, Form()]):

    if type not in tradeTypes:
        print(f"Ignore order because type is not handled: {type}")
        return

    print("Updating...")
    modifySignalInDb(id, type, entry, sl, tp, lots)

    return "Order modified"

@app.get("/linesinfo/")
async def linesInfo(symbol:str, timeframe: str):

    if symbol not in symbols:
        print(f"Ignore request because symbol is not handled yet: {symbol}")
        return

    timeframeEnum: TimeFrame = TimeFrame.__dict__[timeframe]

    if TimeFrame.PERIOD_D1 is not timeframeEnum and TimeFrame.PERIOD_H4 is not timeframeEnum and TimeFrame.PERIOD_H1 is not timeframeEnum:
        return f"For {timeframeEnum} no line information was greated!!!"

    print("Loading linesinfo at %s for TF %s" % (datetime.datetime.now(), timeframeEnum))
    result = getLinesInfo(symbol, timeframeEnum)

    if len(result) > 0:
        return {'startTime': result[0].startTime, 'endTime': result[0].endTime, 'startValue': result[0].startValue, 'endValue': result[0].endValue}

    return {}

@app.get("/srlevels/")
async def srlevels(symbol:str):

    if symbol not in symbols:
        print(f"Ignore request because symbol is not handled yet: {symbol}")
        return

    result = getSrLevels(symbol)

    if len(result) > 0:
        json_compatible_item_data = jsonable_encoder(result)
        return json.dumps(json_compatible_item_data)

    return {}

# TODO Implement this in Mojo
# and store values to db
# Continue here:
    #https://www.youtube.com/@Algovibes/videos
    #https://www.youtube.com/watch?v=XK2IU5vRJr0
    #https://www.youtube.com/@CodeTradingCafe/videos

@app.post("/updatesignal")
async def updateSignal(signalUpdateDto:SignalUpdateDto):
    if signalUpdateDto.symbol not in symbols:
        print(f"Ignore request because symbol is not handled yet: {signalUpdateDto}")
        return
    updateSignalInDb(signalUpdateDto)
    #TODO send information to clients

@app.post("/updatesignalprod")
async def updateSignalProd(signalUpdateDto:SignalUpdateDto):
    if signalUpdateDto.symbol not in symbols:
        print(f"Ignore request because symbol is not handled yet: {signalUpdateDto}")
        return
    updateSignalProdInDb(signalUpdateDto)
    #TODO send information to clients

@app.post("/updatehistory")
async def updateHistory(historyUpdateDto:HistoryUpdateDto):
    if historyUpdateDto.symbol not in symbols:
        print(f"Ignore request because symbol is not handled yet: {historyUpdateDto}")
        return
    updateSignalByHistory(historyUpdateDto)
    #TODO send information to clients

@app.get("/insertTrades")
def insertTrades():
    if countTrades() == 0:
        insertFromFile("sql/Trades.csv")
        return countTrades()
    else:
        return countTrades()

@app.post("/signalactivated")
async def signalActivated(signalActivation:SignalActivationDto):
    if signalActivation.symbol not in symbols:
        print(f"Ignore request because symbol is not handled yet: {signalActivation}")
        return

    activateSignal(signalActivation)
    #TODO send information to clients

@app.post("/storecandle")
async def storeCandle(candle:CandlesDto):
    if candle.symbol not in symbols:
        print(f"Ignore request because symbol is not handled yet: {candle}")
        return

    timeframeEnum: TimeFrame = TimeFrame.__dict__[candle.TIMEFRAME]

    if timeframeEnum != TimeFrame.PERIOD_M1:
        storeCandleInDb(candle)
    json_compatible_item_data = jsonable_encoder(candle)
    await manager.broadcast(json.dumps(json_compatible_item_data))

def autoDetectSupportAndResistance(symbol:str, sliceMax:int, peaksMax:int, timeFrame: TimeFrame):

    slice_ = slice(10, sliceMax)
    peaks_range = [2, peaksMax]
    num_peaks = -999

    df = loadDfFromDb(symbol, timeFrame)
    sample = df.iloc[slice_][['CLOSE']].to_numpy().flatten()

    maxima = argrelextrema(sample, np.greater)
    minima = argrelextrema(sample, np.less)

    extrema_prices = np.concatenate((sample[maxima], sample[minima]))
    interval = extrema_prices[0]/10000

    bandwidth = interval

    while num_peaks < peaks_range[0] or num_peaks > peaks_range[1]:
        kde = KernelDensity(kernel='gaussian', bandwidth=bandwidth).fit(extrema_prices.reshape(-1, 1))
        a,b = min(extrema_prices), max(extrema_prices)
        price_range = np.linspace(a, b, 1000).reshape(-1,1)
        pdf = np.exp(kde.score_samples(price_range))
        peaks = find_peaks(pdf)[0]
        num_peaks = len(peaks)
        bandwidth += interval

        if bandwidth > 100*interval:
            print("Failed to converge, stopping ...")
            break


    actualPrice = df.iloc[-1]['CLOSE']
    prices = []
    for price in price_range[peaks]:
        prices.append(float(price))
        type = SupportResistanceType.SUPPORT
        if actualPrice < float(price):
            type = SupportResistanceType.RESISTANCE

        storeSupportResistance(
            SupportResistance(
                symbol=symbol,
                timeframe=timeFrame,
                level=float(price),
                type=type,
                caclulator="defaultsr"
            )
        )

    return {
        'prices': prices
    }

def defaultsr(symbol:str, diff:float, timeFrame: TimeFrame):

    startDate: str = '2015.01.02'

    start = timer()

    df_org = loadDfFromDb(symbol, timeFrame)
    mask = (df_org['DATETIME'] >= startDate)
    df = df_org.loc[mask]
    actualLevel = df.iloc[-1]['CLOSE']

    dfLows = df.loc[df.LOW < actualLevel]
    dfHighs = df.loc[df.HIGH > actualLevel]

    supports = dfLows[dfLows.LOW == dfLows.LOW.rolling(5, center=True).min()].LOW
    resistances = dfHighs[dfHighs.HIGH == dfHighs.HIGH.rolling(5, center=True).max()].HIGH
    #print(supports)

    #print("supports:", len(supports))
    #print("supports:", supports.head(10))
    #print("resistances:", len(resistances))
    #print("resistances:", resistances.head(60))
    
    levels = pd.concat([supports, resistances])

    # Filter
    levels = levels[abs(levels.diff() > diff)]

    finalSupports = levels[levels < actualLevel]
    finalResistances = levels[levels > actualLevel]
    #print(finalResistances)
    #print(finalSupports)
    
    end = timer()
    print(timedelta(seconds=end-start))

    #return finalSupports.combine(finalResistances, min)
    #return pd.concat([finalSupports, finalResistances], axis=1)
    #return finalSupports.to_frame().join(finalResistances.to_frame())
    # TODO nee to transform to json

    levelsDf = pd.DataFrame(dict(supports = finalSupports, resistances = finalResistances)).reset_index()

    supportLevels = levelsDf[levelsDf.supports.notnull()].sort_values(by='supports', ascending=False).head(4).supports.to_list()

    for support in supportLevels:
        storeSupportResistance(
            SupportResistance(
                symbol=symbol,
                timeframe=timeFrame,
                level=support,
                type=SupportResistanceType.SUPPORT,
                caclulator="defaultsr"
            )
        )
    resistanceLevels = levelsDf[levelsDf.resistances.notnull()].sort_values(by='resistances', ascending=True).head(4).resistances.to_list()
    for resistance in resistanceLevels:
        storeSupportResistance(
            SupportResistance(
                symbol=symbol,
                timeframe=timeFrame,
                level=resistance,
                type=SupportResistanceType.RESISTANCE,
                caclulator="defaultsr"
            )
        )

    return {
        'supports': supportLevels,
        'resistances': resistanceLevels
    }

#https://www.youtube.com/watch?v=5OjX8r3DsmU
def trendlinebreakout(symbol:str, timeFrame: TimeFrame):
    data = loadDfFromDb(symbol, timeFrame)

    data = data.set_index('DATETIME')
    data = data.dropna()
    data['Open'] = data.OPEN
    data['High'] = data.HIGH
    data['Low'] = data.LOW
    data['close'] = data.CLOSE
    data['Volume'] = data.TICKVOL

    lookback = 200
    support, resist, signal = trendline_breakout(data['close'].to_numpy(), lookback)

    storeSupportResistance(
        SupportResistance(
            symbol=symbol,
            timeframe=timeFrame,
            level= support[len(support)-1],
            type=SupportResistanceType.RESISTANCE,
            caclulator="trendlinebreakout"
        )
    )

    storeSupportResistance(
        SupportResistance(
            symbol=symbol,
            timeframe=timeFrame,
            level= resist[len(resist)-1],
            type=SupportResistanceType.RESISTANCE,
            caclulator="trendlinebreakout"
        )
    )

    return {
        'support': support[len(support)-1],
        'resistance': resist[len(resist)-1],
        'signal': signal[len(signal)-1]
    }

def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

def job():

    # TODO needs timeframe

    now = datetime.datetime.now()
    hour = now.hour

    for symbol in symbols:
        for timeFrame in TimeFrame:
            if TimeFrame.PERIOD_H1 is timeFrame or TimeFrame.PERIOD_H4 is timeFrame:
                deleteSupportResistance(symbol, timeFrame)
                regressionCalculation(symbol,startDate, timeFrame)
                trendlinebreakout(symbol, timeFrame)
                autoDetectSupportAndResistance(symbol, 30000, 20, timeFrame)
                defaultsr(symbol, 0.01, timeFrame)

    if hour == 0:

        for symbol in symbols:
            for timeFrame in TimeFrame:
                if TimeFrame.PERIOD_D1 is timeFrame:
                    deleteSupportResistance(symbol, timeFrame)
                    regressionCalculation(symbol,startDate, timeFrame)
                    trendlinebreakout(symbol, timeFrame)
                    autoDetectSupportAndResistance(symbol, 30000, 20, timeFrame)
                    defaultsr(symbol, 0.01, timeFrame)

    #TODO how to get end/start of the week?


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    root = logging.getLogger()
    hdlr = root.handlers[0]
    json_format = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')
    hdlr.setFormatter(json_format)
    #dropAllTables()
    initTradingDb()

    #if countTrades() == 0:
    #    insertFromFile("sql/Trades.csv")
    #else:
    #    print(str(countTrades()) + " Trades stored!")

    # NUR wenn DB leer bzw. für Kombination aus Symbol + Timeframe kein Eintrag
    # gefunden wird
    for symbol in symbols:
        for timeFrame in TimeFrame:
            if TimeFrame.PERIOD_M1 is not timeFrame:
                if countEntries(symbol,timeFrame) == 0:
                    last = lastCandle(symbol, timeFrame)
                    if last is None:
                        storeData(symbol,timeFrame)
                        #loadDfFromDb(symbol, timeFrame)
                        print(f"Inserted data for {symbol} + {timeFrame}")

    #TODO on startup go through like this load the last candle and from this candle on load all until now other metatrade
    for symbol in symbols:
       for timeFrame in TimeFrame:
            if TimeFrame.PERIOD_H1 is timeFrame or TimeFrame.PERIOD_H4 is timeFrame or TimeFrame.PERIOD_D1 is timeFrame or TimeFrame.PERIOD_W1 is timeFrame:
                deleteSupportResistance(symbol, timeFrame)
                trendlinebreakout(symbol, timeFrame)
                autoDetectSupportAndResistance(symbol, 30000, 20, timeFrame)
                defaultsr(symbol, 0.01, timeFrame)
                regressionCalculation(symbol,startDate, timeFrame)

    schedule.every().hour.do(job)
    #schedule.every().hour.do(runFirstStrategy)
    # Start the background thread
    stop_run_continuously = run_continuously()
    uvicorn.run(app, host="0.0.0.0", port=6081)

    #consumer.subscribe(['test:1:1'])

    #for message in consumer:
    #    receivedMsg(message)