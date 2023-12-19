import logging
import datetime
import json
import threading
import time
from datetime import timedelta
from timeit import default_timer as timer
from typing import List
import requests
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
    activateSignal, activateSignalProd, SignalUpdateDto, updateSignalInDb, updateSignalProdInDb, modifySignalInDb, \
    deleteSignalInDb, tradeTypes, \
    getExecutedSignals, HistoryUpdateDto, updateSignalByHistory, getStrategystats, getIgnoredSignals, TimeFrame, \
    getLinesInfo, regressionCalculation, lastCandle, CandlesDto, loadDfFromDb, storeCandleInDb, countEntries, storeData, \
    getSrLevels, SupportResistanceType, storeSupportResistance, SupportResistance, deleteSupportResistance, \
    getInstrumentstats, deleteSignalFromDb, SignalId, deleteIgnoredSignalFromDb, getWaitingSignalsProd, countSignals
from pinescripts import f_LazyLine, tThree
from trading_strategies.adx_crossover import AdxCrossover
from trading_strategies.adx_ema_14 import ADXEMA14
from trading_strategies.adx_rsi import AdxRsi
from trading_strategies.aroon_adx import AroonAdx
from trading_strategies.aroon_indicator import AroonIndicator
from trading_strategies.awesome_saucer import AwesomeOscillatorSaucer
from trading_strategies.awesome_zero_crossover import AwesomeOscillatorZeroCrossover
from trading_strategies.blade_runner import BladeRunner
from trading_strategies.bollingerbands_rsi import BollingerBandsAndRSI
from trading_strategies.bollingerbands_rsi_2 import BollingerBandsAndRSI2
from trading_strategies.cci_macd_psar import CciMacdPsar
from trading_strategies.cci_moving_average import CciMovingAverage
from trading_strategies.commodity_channel_index import CommodityChannelIndex
from trading_strategies.donchian_atr import DonchianATR
from trading_strategies.donchian_breakout import DonchianBreakout
from trading_strategies.donchian_middle import DonchianMiddle
from trading_strategies.dpo_candlestick import DpoCandlestick
from trading_strategies.elder_ray import ElderRay
from trading_strategies.elder_ray_alternative import ElderRayAlternative
from trading_strategies.ema_3 import ThreeEma
from trading_strategies.ema_3_alternative import ThreeEmaAlternative
from trading_strategies.ema_crossover import EMACrossover
from trading_strategies.ema_crossover_alternative import EMACrossoverAlternative
from trading_strategies.ema_crossover_macd import EMACrossoverMACD
from trading_strategies.ema_crossover_rsi import EMACrossoverRSI
from trading_strategies.ema_crossover_rsi_alternative import EMACrossoverRSIAlternative
from trading_strategies.ema_macd_rsi import EMAMACDRSI
from trading_strategies.ema_mi import EMAMI
from trading_strategies.force_index_ema import ForceIndexEMA
from trading_strategies.k_stoch_adx import KeltnerStochasticAdx
from trading_strategies.kama import KAMA
from trading_strategies.kama_crossover import KAMACrossover
from trading_strategies.keltner_adx import KeltnerAdx
from trading_strategies.keltner_rsi import KeltnerRsi
from trading_strategies.keltner_stochastic import KeltnerStochastic
from trading_strategies.macd_crossover import MACDCrossover
from trading_strategies.macd_histogram_reversal import MACDHistogramReversal
from trading_strategies.macd_rsi_sma import MacdRsiSma
from trading_strategies.macd_stochastic_crossover import MACDStochasticCrossover
from trading_strategies.macd_zero_cross import MACDZeroCross
from trading_strategies.mfi import MFI
from trading_strategies.oops_signals import OopsSignals
from trading_strategies.psar_moving_average import PsarMovingAverage
from trading_strategies.rsi_2 import Rsi2
from trading_strategies.rsi_80_20 import Rsi8020
from trading_strategies.sma_ema import SimpleMAExponentialMA
from trading_strategies.sma_ema_alternative import SimpleMAExponentialMAAlternative
from trading_strategies.sma_mi import SMAMI
from trading_strategies.stochastic_oscillator_no_exit import StochasticOscillatorNoExit
from trading_strategies.triple_bollingerbands import TripleBollingerBands
from trading_strategies.trix_ema import TrixEma
from trading_strategies.trix_mi import TrixMI
from trading_strategies.trix_rsi import TrixRsi
from trading_strategies.tsi_crossover import TSICrossover
from trading_strategies.vortex_crossover import VortexCrossover
from trading_strategies.vortex_sma import VortexSma
from trading_strategies.williams_r_sma import WilliamsIndicator
from trading_strategies.williams_rsi import WilliamsRsi
from trading_strategies.williams_stochastic import WilliamsStochastic
from trading_strategies.zig_zag import ZigZag
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

#def process_row(index, row):
#    print(f"Processing row {index} - DATETIME: {row['DATETIME']}, Close: {row['close']}, TIMEFRAME: {row['TIMEFRAME']}")

@app.get("/redkslow/")
async def redkslow(symbol:str, timeframe: str):

    if symbol not in symbols:
        print(f"Ignore request because symbol is not handled yet: {symbol}")
        return

    timeframeEnum: TimeFrame = TimeFrame.__dict__[timeframe]

    if TimeFrame.PERIOD_D1 is not timeframeEnum and TimeFrame.PERIOD_H4 is not timeframeEnum and TimeFrame.PERIOD_H1 is not timeframeEnum:
        return f"For {timeframeEnum} no line information was greated!!!"

    print("Calculating redkslow for %s-%s" % (symbol, timeframeEnum))
    data = loadDfFromDb(symbol, timeframeEnum)

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

    #print("++++++++++++++++++")
    #print(data['redkslow'])
    #print(data['redkslow'].shift(1))
    #print(data['close'].tail(-1).tail(200))
    #print(data['close'].iloc[len(data)-200:len(data)-1])
    #print("++++++++++++++++++")
    #print(f"{LL}")
    #print(f"{LLPrev}")
    #print("++++++++++++++++++")

    #uptrend     = LL > LL[1]
    #SwingDn = uptrend[1] and not uptrend
    #SwingUp = uptrend and not uptrend[1]

    return {'ll': LL, 'llprev': LLPrev}

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


#@app.get("/insertTrades")
#def insertTrades():
#    if countTrades() == 0:
#        insertFromFile("sql/Trades.csv")
#        return countTrades()
#    else:
#        return countTrades()

@app.post("/signalactivated")
async def signalActivated(signalActivation:SignalActivationDto):
    if signalActivation.symbol not in symbols:
        print(f"Ignore request because symbol is not handled yet: {signalActivation}")
        return

    activateSignal(signalActivation)

@app.post("/signalactivatedprod")
async def signalActivatedProd(signalActivation:SignalActivationDto):
    if signalActivation.symbol not in symbols:
        print(f"Ignore request because symbol is not handled yet: {signalActivation}")
        return

    activateSignalProd(signalActivation)


def postSignal(symbol, timeframeEnum, type, strategy, entry):
    count = countSignals(strategy + str(timeframeEnum).replace("PERIOD", ""), symbol)
    if count == 0:
        #signal:SignalDto
        data = {"symbol": symbol,
                "timestamp": str(timeframeEnum),
                "type": type,
                "entry": entry,
                "sl": 0,
                "tp": 0,
                "strategy": strategy + str(timeframeEnum).replace("PERIOD", "")}
        response = requests.post(
            "http://tvsignals:80/signal/",
            json=data,
        )
        print(str(response.status_code))

def adx(df, symbol, timeframeEnum, entry):
    strategy = AdxCrossover(df)
    signal_lst, df = strategy.run()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "AdxCrossover", entry)
    elif signal == -1:
        postSignal(symbol, timeframeEnum, "sell", "AdxCrossover", entry)


def adxEma14(df, symbol, timeframeEnum, entry):
    strategy = ADXEMA14(df)
    signal_lst, df = strategy.run_adx_ema_14()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "ADXEMA14", entry)
    elif signal == -1:
        print("Short on ADXEMA14")


def adxRsi(df, symbol, timeframeEnum, entry):
    strategy = AdxRsi(df)
    signal_lst, df = strategy.run_adx_rsi()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "AdxRsi", entry)
    elif signal == -1:
        print("Short on AdxRsi")


def aroonAdx(df, symbol, timeframeEnum, entry):
    strategy = AroonAdx(df)
    signal_lst, df = strategy.run_aroon_adx()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "AroonAdx", entry)
    elif signal == -1:
        print("Short on AroonAdx")

def aroonIndicator(df, symbol, timeframeEnum, entry):
    strategy = AroonIndicator(df)
    signal_lst, df = strategy.run_aroon_indicator()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "AroonIndicator", entry)
    elif signal == -1:
        print("Short on AroonIndicator")


def awesomeOscillatorSaucer(df, symbol, timeframeEnum, entry):
    strategy = AwesomeOscillatorSaucer(df)
    signal_lst, df = strategy.run_awesome_oscillator_saucer()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "AwesomeOscillatorSaucer", entry)
    elif signal == -1:
        print("Short on AwesomeOscillatorSaucer")


def awesomeOscillatorZeroCrossover(df, symbol, timeframeEnum, entry):
    strategy = AwesomeOscillatorZeroCrossover(df)
    signal_lst, df = strategy.run_awesome_oscillator_zero_crossover()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "AwesomeOscillatorSaucer", entry)
    elif signal == -1:
        print("Short on AwesomeOscillatorZeroCrossover")


def bladeRunner(df, symbol, timeframeEnum, entry):
    strategy = BladeRunner(df)
    signal_lst, df = strategy.run_blade_runner()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "BladeRunner", entry)
    elif signal == -1:
        print("Short on BladeRunner")


def bollingerBandsAndRSI(df, symbol, timeframeEnum, entry):
    strategy = BollingerBandsAndRSI(df)
    signal_lst, df = strategy.run_bollingerbands_rsi()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "BollingerBandsAndRSI", entry)
    elif signal == -1:
        print("Short on BollingerBandsAndRSI")


def bollingerBandsAndRSI2(df, symbol, timeframeEnum, entry):
    strategy = BollingerBandsAndRSI2(df)
    signal_lst, df = strategy.run_bollingerbands_rsi_2()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "BollingerBandsAndRSI2", entry)
    elif signal == -1:
        print("Short on BollingerBandsAndRSI2")


def cciMacdPsar(df, symbol, timeframeEnum, entry):
    strategy = CciMacdPsar(df)
    signal_lst, df = strategy.run()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "CciMacdPsar", entry)
    elif signal == -1:
        print("Short on CciMacdPsar")


def cciMovingAverage(df, symbol, timeframeEnum, entry):
    strategy = CciMovingAverage(df)
    signal_lst, df = strategy.run()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "CciMovingAverage", entry)
    elif signal == -1:
        print("Short on CciMovingAverage")


def commodityChannelIndex(df, symbol, timeframeEnum, entry):
    strategy = CommodityChannelIndex(df)
    signal_lst, df = strategy.run()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "CommodityChannelIndex", entry)
    elif signal == -1:
        print("Short on CommodityChannelIndex")

def donchianATR(df, symbol, timeframeEnum, entry):
    strategy = DonchianATR(df)
    signal_lst, df = strategy.run_donchian_atr()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "DonchianATR", entry)
    elif signal == -1:
        print("Short on DonchianATR")


def donchianBreakout(df, symbol, timeframeEnum, entry):
    strategy = DonchianBreakout(df)
    signal_lst, df = strategy.run_donchian_breakout()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "DonchianBreakout", entry)
    elif signal == -1:
        print("Short on DonchianBreakout")


def donchianMiddle(df, symbol, timeframeEnum, entry):
    strategy = DonchianMiddle(df)
    signal_lst, df = strategy.run_donchian_middle()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "DonchianMiddle", entry)
    elif signal == -1:
        print("Short on DonchianMiddle")


def dpoCandlestick(df, symbol, timeframeEnum, entry):
    strategy = DpoCandlestick(df)
    signal_lst, df = strategy.run_dpo_candlestick()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "DpoCandlestick", entry)
    elif signal == -1:
        print("Short on DpoCandlestick")


def elderRay(df, symbol, timeframeEnum, entry):
    strategy = ElderRay(df)
    signal_lst, df = strategy.run_elder_ray()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "ElderRay", entry)
    elif signal == -1:
        print("Short on ElderRay")


def elderRayAlternative(df, symbol, timeframeEnum, entry):
    strategy = ElderRayAlternative(df)
    signal_lst, df = strategy.run_elder_ray()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "ElderRayAlternative", entry)
    elif signal == -1:
        print("Short on ElderRayAlternative")


def threeEma(df, symbol, timeframeEnum, entry):
    strategy = ThreeEma(df)
    signal_lst, df = strategy.run_ema_3()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "ThreeEma", entry)
    elif signal == -1:
        print("Short on ThreeEma")


def threeEmaAlternative(df, symbol, timeframeEnum, entry):
    strategy = ThreeEmaAlternative(df)
    signal_lst, df = strategy.run_ema_3()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "ThreeEmaAlternative", entry)
    elif signal == -1:
        print("Short on ThreeEmaAlternative")


def eMACrossover(df, symbol, timeframeEnum, entry):
    strategy = EMACrossover(df)
    signal_lst, df = strategy.run_ema_crossover()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "EMACrossover", entry)
    elif signal == -1:
        print("Short on EMACrossover")


def eMACrossoverAlternative(df, symbol, timeframeEnum, entry):
    strategy = EMACrossoverAlternative(df)
    signal_lst, df = strategy.run_ema_crossover()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "EMACrossoverAlternative", entry)
    elif signal == -1:
        print("Short on EMACrossoverAlternative")


def eMACrossoverMACD(df, symbol, timeframeEnum, entry):
    strategy = EMACrossoverMACD(df)
    signal_lst, df = strategy.run_ema_crossover_macd()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "EMACrossoverMACD", entry)
    elif signal == -1:
        print("Short on EMACrossoverMACD")


def eMACrossoverRSI(df, symbol, timeframeEnum, entry):
    strategy = EMACrossoverRSI(df)
    signal_lst, df = strategy.run_ema_crossover_rsi()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "EMACrossoverRSI", entry)
    elif signal == -1:
        print("Short on EMACrossoverRSI")


def eMACrossoverRSIAlternative(df, symbol, timeframeEnum, entry):
    strategy = EMACrossoverRSIAlternative(df)
    signal_lst, df = strategy.run_ema_crossover_rsi()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "EMACrossoverRSIAlternative", entry)
    elif signal == -1:
        print("Short on EMACrossoverRSIAlternative")


def eMAMACDRSI(df, symbol, timeframeEnum, entry):
    strategy = EMAMACDRSI(df)
    signal_lst, df = strategy.run_ema_macd_rsi()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "EMAMACDRSI", entry)
    elif signal == -1:
        print("Short on EMAMACDRSI")


def eMAMI(df, symbol, timeframeEnum, entry):
    strategy = EMAMI(df)
    signal_lst, df = strategy.run()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "EMAMI", entry)
    elif signal == -1:
        print("Short on EMAMI")


def forceIndexEMA(df, symbol, timeframeEnum, entry):
    strategy = ForceIndexEMA(df)
    signal_lst, df = strategy.run_force_index()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "ForceIndexEMA", entry)
    elif signal == -1:
        print("Short on ForceIndexEMA")


def keltnerStochasticAdx(df, symbol, timeframeEnum, entry):
    strategy = KeltnerStochasticAdx(df)
    signal_lst, df = strategy.run_keltner_stochastic_adx()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "KeltnerStochasticAdx", entry)
    elif signal == -1:
        print("Short on KeltnerStochasticAdx")


def kAMA(df, symbol, timeframeEnum, entry):
    strategy = KAMA(df)
    signal_lst, df = strategy.run_kama()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "KAMA", entry)
    elif signal == -1:
        print("Short on KAMA")


def kAMACrossover(df, symbol, timeframeEnum, entry):
    strategy = KAMACrossover(df)
    signal_lst, df = strategy.run()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "KAMACrossover", entry)
    elif signal == -1:
        print("Short on KAMACrossover")


def keltnerAdx(df, symbol, timeframeEnum, entry):
    strategy = KeltnerAdx(df)
    signal_lst, df = strategy.run_keltner_adx()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "KeltnerAdx", entry)
    elif signal == -1:
        print("Short on KeltnerAdx")


def keltnerRsi(df, symbol, timeframeEnum, entry):
    strategy = KeltnerRsi(df)
    signal_lst, df = strategy.run_keltner_rsi2()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "KeltnerRsi", entry)
    elif signal == -1:
        print("Short on KeltnerRsi")


def keltnerStochastic(df, symbol, timeframeEnum, entry):
    strategy = KeltnerStochastic(df)
    signal_lst, df = strategy.run_keltner_stochastic()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "KeltnerStochastic", entry)
    elif signal == -1:
        print("Short on KeltnerStochastic")


def mACDCrossover(df, symbol, timeframeEnum, entry):
    strategy = MACDCrossover(df)
    signal_lst, df = strategy.run_macd_crossover()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "MACDCrossover", entry)
    elif signal == -1:
        print("Short on MACDCrossover")


def mACDHistogramReversal(df, symbol, timeframeEnum, entry):
    strategy = MACDHistogramReversal(df)
    signal_lst, df = strategy.run_macd_histogram_reversal()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "MACDHistogramReversal", entry)
    elif signal == -1:
        print("Short on MACDHistogramReversal")


def macdRsiSma(df, symbol, timeframeEnum, entry):
    strategy = MacdRsiSma(df)
    signal_lst, df = strategy.run_macd_rsi_sma()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "MacdRsiSma", entry)
    elif signal == -1:
        print("Short on MacdRsiSma")


def mACDStochasticCrossover(df, symbol, timeframeEnum, entry):
    strategy = MACDStochasticCrossover(df)
    signal_lst, df = strategy.run_macd_stochastic_crossover()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "MACDStochasticCrossover", entry)
    elif signal == -1:
        print("Short on MACDStochasticCrossover")


def mACDZeroCross(df, symbol, timeframeEnum, entry):
    strategy = MACDZeroCross(df)
    signal_lst, df = strategy.run_macd_zero_cross()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "MACDZeroCross", entry)
    elif signal == -1:
        print("Short on MACDZeroCross")


def mFI(df, symbol, timeframeEnum, entry):
    strategy = MFI(df)
    signal_lst, df = strategy.run()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "MFI", entry)
    elif signal == -1:
        print("Short on MFI")


def oopsSignals(df, symbol, timeframeEnum, entry):
    strategy = OopsSignals(df)
    signal_lst, df = strategy.run_oops_signals()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "OopsSignals", entry)
    elif signal == -1:
        print("Short on OopsSignals")


def psarMovingAverage(df, symbol, timeframeEnum, entry):
    strategy = PsarMovingAverage(df)
    signal_lst, df = strategy.run_psar_moving_average()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "PsarMovingAverage", entry)
    elif signal == -1:
        print("Short on PsarMovingAverage")


def rsi2(df, symbol, timeframeEnum, entry):
    strategy = Rsi2(df)
    signal_lst, df = strategy.run_rsi2()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "Rsi2", entry)
    elif signal == -1:
        print("Short on Rsi2")


def rsi8020(df, symbol, timeframeEnum, entry):
    strategy = Rsi8020(df)
    signal_lst, df = strategy.run_rsi_80_20()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "Rsi8020", entry)
    elif signal == -1:
        postSignal(symbol, timeframeEnum, "sell", "Rsi8020", entry)

def simpleMAExponentialMA(df, symbol, timeframeEnum, entry):
    strategy = SimpleMAExponentialMA(df)
    signal_lst, df = strategy.run_sma_ema()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "SimpleMAExponentialMA", entry)
    elif signal == -1:
        postSignal(symbol, timeframeEnum, "sell", "SimpleMAExponentialMA", entry)


def simpleMAExponentialMAAlternative(df, symbol, timeframeEnum, entry):
    strategy = SimpleMAExponentialMAAlternative(df)
    signal_lst, df = strategy.run_sma_ema()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "SimpleMAExponentialMAAlternative", entry)
    elif signal == -1:
        postSignal(symbol, timeframeEnum, "sell", "SimpleMAExponentialMAAlternative", entry)


def sMAMI(df, symbol, timeframeEnum, entry):
    strategy = SMAMI(df)
    signal_lst, df = strategy.run()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "SMAMI", entry)
    elif signal == -1:
        postSignal(symbol, timeframeEnum, "sell", "SMAMI", entry)


def stochasticOscillatorNoExit(df, symbol, timeframeEnum, entry):
    strategy = StochasticOscillatorNoExit(df)
    signal_lst, df = strategy.run_stochastic_oscillator_no_exit()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "StochasticOscillatorNoExit", entry)
    elif signal == -1:
        postSignal(symbol, timeframeEnum, "sell", "StochasticOscillatorNoExit", entry)


def tripleBollingerBands(df, symbol, timeframeEnum, entry):
    strategy = TripleBollingerBands(df)
    signal_lst, df = strategy.run_triple_bollinger_bands()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "TripleBollingerBands", entry)
    elif signal == -1:
        postSignal(symbol, timeframeEnum, "sell", "TripleBollingerBands", entry)


def trixEma(df, symbol, timeframeEnum, entry):
    strategy = TrixEma(df)
    signal_lst, df = strategy.run_trix_ema()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "TrixEma", entry)
    elif signal == -1:
        postSignal(symbol, timeframeEnum, "sell", "TrixEma", entry)


def trixMI(df, symbol, timeframeEnum, entry):
    strategy = TrixMI(df)
    signal_lst, df = strategy.run()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "TrixMI", entry)
    elif signal == -1:
        postSignal(symbol, timeframeEnum, "sell", "TrixMI", entry)


def trixRsi(df, symbol, timeframeEnum, entry):
    strategy = TrixRsi(df)
    signal_lst, df = strategy.run_trix_rsi()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "TrixRsi", entry)
    elif signal == -1:
        postSignal(symbol, timeframeEnum, "sell", "TrixRsi", entry)


def tSICrossover(df, symbol, timeframeEnum, entry):
    strategy = TSICrossover(df)
    signal_lst, df = strategy.run_tsi_crossover()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "TSICrossover", entry)
    elif signal == -1:
        postSignal(symbol, timeframeEnum, "sell", "TSICrossover", entry)


def vortexCrossover(df, symbol, timeframeEnum, entry):
    strategy = VortexCrossover(df)
    signal_lst, df = strategy.run()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "VortexCrossover", entry)
    elif signal == -1:
        postSignal(symbol, timeframeEnum, "sell", "VortexCrossover", entry)


def vortexSma(df, symbol, timeframeEnum, entry):
    strategy = VortexSma(df)
    signal_lst, df = strategy.run_vortex_sma()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "VortexSma", entry)
    elif signal == -1:
        postSignal(symbol, timeframeEnum, "sell", "VortexSma", entry)


def williamsIndicator(df, symbol, timeframeEnum, entry):
    strategy = WilliamsIndicator(df)
    signal_lst, df = strategy.run_williams_indicator()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "WilliamsIndicator", entry)
    elif signal == -1:
        postSignal(symbol, timeframeEnum, "sell", "WilliamsIndicator", entry)


def williamsRsi(df, symbol, timeframeEnum, entry):
    strategy = WilliamsRsi(df)
    signal_lst, df = strategy.run_williams_indicator()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "WilliamsRsi", entry)
    elif signal == -1:
        postSignal(symbol, timeframeEnum, "sell", "WilliamsRsi", entry)


def williamsStochastic(df, symbol, timeframeEnum, entry):
    strategy = WilliamsStochastic(df)
    signal_lst, df = strategy.run_williams_stochastic()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "WilliamsStochastic", entry)
    elif signal == -1:
        postSignal(symbol, timeframeEnum, "sell", "WilliamsStochastic", entry)


def zigZag(df, symbol, timeframeEnum, entry):
    strategy = ZigZag(df)
    signal_lst, df = strategy.run_zigzag()
    signal = signal_lst[0]
    if signal == 1:
        postSignal(symbol, timeframeEnum, "buy", "ZigZag", entry)
    elif signal == -1:
        postSignal(symbol, timeframeEnum, "sell", "ZigZag", entry)


@app.post("/storecandle")
async def storeCandle(candle:CandlesDto):
    symbol = candle.symbol
    if symbol not in symbols:
        print(f"Ignore request because symbol is not handled yet: {candle}")
        return

    timeframeEnum: TimeFrame = TimeFrame.__dict__[candle.TIMEFRAME]

    if timeframeEnum != TimeFrame.PERIOD_M1:
        #storeCandleInDb(candle)
        #Call strategies

        df = loadDfFromDb(symbol, timeframeEnum, 10000)
        df['open'] = df.OPEN
        df['high'] = df.HIGH
        df['low'] = df.LOW
        df['close'] = df.CLOSE
        df['volume'] = df.TICKVOL
        df['vol'] = df.TICKVOL
        entry = df.iloc[-1].CLOSE
        adx(df, symbol, timeframeEnum, entry)
        adxEma14(df, symbol, timeframeEnum, entry)
        adxRsi(df, symbol, timeframeEnum, entry)
        #aroonAdx(df)
        #aroonIndicator(df)
        awesomeOscillatorSaucer(df, symbol, timeframeEnum, entry)
        awesomeOscillatorZeroCrossover(df, symbol, timeframeEnum, entry)
        bladeRunner(df, symbol, timeframeEnum, entry)
        bollingerBandsAndRSI(df, symbol, timeframeEnum, entry)
        bollingerBandsAndRSI2(df, symbol, timeframeEnum, entry)
        cciMacdPsar(df, symbol, timeframeEnum, entry)
        cciMovingAverage(df, symbol, timeframeEnum, entry)
        commodityChannelIndex(df, symbol, timeframeEnum, entry)
        donchianATR(df, symbol, timeframeEnum, entry)
        donchianBreakout(df, symbol, timeframeEnum, entry)
        donchianMiddle(df, symbol, timeframeEnum, entry)
        dpoCandlestick(df, symbol, timeframeEnum, entry)
        #elderRay(df)
        #elderRayAlternative(df)
        threeEma(df, symbol, timeframeEnum, entry)
        threeEmaAlternative(df, symbol, timeframeEnum, entry)
        eMACrossover(df, symbol, timeframeEnum, entry)
        eMACrossoverAlternative(df, symbol, timeframeEnum, entry)
        eMACrossoverMACD(df, symbol, timeframeEnum, entry)
        eMACrossoverRSI(df, symbol, timeframeEnum, entry)
        eMACrossoverRSIAlternative(df, symbol, timeframeEnum, entry)
        eMAMACDRSI(df, symbol, timeframeEnum, entry)
        eMAMI(df, symbol, timeframeEnum, entry)
        #forceIndexEMA(df)
        keltnerStochasticAdx(df, symbol, timeframeEnum, entry)
        kAMA(df, symbol, timeframeEnum, entry)
        kAMACrossover(df, symbol, timeframeEnum, entry)
        keltnerAdx(df, symbol, timeframeEnum, entry)
        keltnerRsi(df, symbol, timeframeEnum, entry)
        keltnerStochastic(df, symbol, timeframeEnum, entry)
        mACDCrossover(df, symbol, timeframeEnum, entry)
        mACDHistogramReversal(df, symbol, timeframeEnum, entry)
        macdRsiSma(df, symbol, timeframeEnum, entry)
        mACDStochasticCrossover(df, symbol, timeframeEnum, entry)
        mACDZeroCross(df, symbol, timeframeEnum, entry)
        #mFI(df, symbol, timeframeEnum)
        #oopsSignals(df, symbol, timeframeEnum)
        psarMovingAverage(df, symbol, timeframeEnum, entry)
        rsi2(df, symbol, timeframeEnum, entry)
        rsi8020(df, symbol, timeframeEnum, entry)
        simpleMAExponentialMA(df, symbol, timeframeEnum, entry)
        simpleMAExponentialMAAlternative(df, symbol, timeframeEnum, entry)
        sMAMI(df, symbol, timeframeEnum, entry)
        stochasticOscillatorNoExit(df, symbol, timeframeEnum, entry)
        #tripleBollingerBands(df, symbol, timeframeEnum)
        trixEma(df, symbol, timeframeEnum, entry)
        trixMI(df, symbol, timeframeEnum, entry)
        #trixRsi(df, symbol, timeframeEnum)
        #tSICrossover(df, symbol, timeframeEnum)
        vortexCrossover(df, symbol, timeframeEnum, entry)
        vortexSma(df, symbol, timeframeEnum, entry)
        williamsIndicator(df, symbol, timeframeEnum, entry)
        williamsRsi(df, symbol, timeframeEnum, entry)
        williamsStochastic(df, symbol, timeframeEnum, entry)
        zigZag(df, symbol, timeframeEnum, entry)

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
    #for symbol in symbols:
    #   for timeFrame in TimeFrame:
    #        if TimeFrame.PERIOD_H1 is timeFrame or TimeFrame.PERIOD_H4 is timeFrame or TimeFrame.PERIOD_D1 is timeFrame or TimeFrame.PERIOD_W1 is timeFrame:
    #            deleteSupportResistance(symbol, timeFrame)
    #            trendlinebreakout(symbol, timeFrame)
    #            autoDetectSupportAndResistance(symbol, 30000, 20, timeFrame)
    #            defaultsr(symbol, 0.01, timeFrame)
    #            regressionCalculation(symbol,startDate, timeFrame)

    schedule.every().hour.do(job)
    #schedule.every().hour.do(runFirstStrategy)
    # Start the background thread
    stop_run_continuously = run_continuously()
    uvicorn.run(app, host="0.0.0.0", port=6081)

    #consumer.subscribe(['test:1:1'])

    #for message in consumer:
    #    receivedMsg(message)