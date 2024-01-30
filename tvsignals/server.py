import enum
import os

import pandas as pd
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request, status, Form
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
# Bellow the import create a job that will be executed on background
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import Enum
from sqlalchemy import String, DateTime, UniqueConstraint
from sqlalchemy import create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import sessionmaker
from typing_extensions import Annotated

load_dotenv()

engine = create_engine(os.environ['POSTGRES_URL'], pool_size=10, max_overflow=0)
Session = sessionmaker(bind=engine)
app = FastAPI()

symbols = ["AUDUSD", "AUDCHF", "AUDJPY", "AUDNZD", "CHFJPY", "EURUSD", "EURCHF", "EURNZD", "GBPUSD", "GBPCAD", "GBPCHF", "GBPNZD",  "XAGUSD", "USDCAD", "USDCHF", "XRPUSD"]
strategies = ["NNR",
              "Super AI Trend",
              "Super AI Trend_WITHOUT_REG",
              "70% Strategy",
              "SSL Hybrid",
              "SSL Hybrid_WITHOUT_REG",
              "AI Volume Supertrend",
              "SSL + Wave Trend Strategy",
              "VHMA",
              "VHMA_WITHOUT_REG",
              "T3Fvma",
              "SentimentRangeMa",
              "SentimentRangeMa_WITHOUT_REG",
              "GaussianChannelTrendAI",
              "T3-LocallyWeightedRegression",
              "T3-HmaKahlman",
              "T3-JMaCrossover",
              "T3-MachineLearningLogisticRegression",
              "T3-machineLearningLogisticRegression",
              "T3-GapFilling",
              "T3-EvwmaVwapMacd",
              "T3-BollingerBandsPinbar",
              "T3-TrendAI",
              "T3-NNFX",
              "T3-EfficientTrendStepMod",
              "T3-AroonBased",
              "T3-AroonBased_WITHOUT_REG",
              "T3-EmaStrategy",
              "T3-EmaStrategy_WITHOUT_REG",
              "SOTT-Lorentzian",
              "RSS_WMA",
              "RSS_WMA_WITHOUT_REG",

              "AdxCrossover_M15",
              "AdxCrossover_H1",
              "AdxCrossover_H4",

              "ADXEMA14_M15",
              "ADXEMA14_H1",
              "ADXEMA14_H4",

              "AdxRsi_M15",
              "AdxRsi_H1",
              "AdxRsi_H4",

              "AroonAdx_M15",
              "AroonAdx_H1",
              "AroonAdx_H4",

              "AroonIndicator_M15",
              "AroonIndicator_H1",
              "AroonIndicator_H4",

              "AwesomeOscillator_M15",
              "AwesomeOscillator_H1",
              "AwesomeOscillator_H4",

              "AwesomeOscillatorSaucer_M15",
              "AwesomeOscillatorSaucer_H1",
              "AwesomeOscillatorSaucer_H4",

              "BladeRunner_M15",
              "BladeRunner_H1",
              "BladeRunner_H4",

              "BollingerBandsAndRSI_M15",
              "BollingerBandsAndRSI_H1",
              "BollingerBandsAndRSI_H4",

              "BollingerBandsAndRSI2_M15",
              "BollingerBandsAndRSI2_H1",
              "BollingerBandsAndRSI2_H4",

              "CciMacdPsar_M15",
              "CciMacdPsar_H1",
              "CciMacdPsar_H4",

              "CciMovingAverage_M15",
              "CciMovingAverage_H1",
              "CciMovingAverage_H4",

              "CommodityChannelIndex_M15",
              "CommodityChannelIndex_H1",
              "CommodityChannelIndex_H4",

              "DonchianATR_M15",
              "DonchianATR_H1",
              "DonchianATR_H4",

              "DonchianBreakout_M15",
              "DonchianBreakout_H1",
              "DonchianBreakout_H4",

              "DonchianMiddle_M15",
              "DonchianMiddle_H1",
              "DonchianMiddle_H4",

              "DpoCandlestick_M15",
              "DpoCandlestick_H1",
              "DpoCandlestick_H4",

              "ElderRay_M15",
              "ElderRay_H1",
              "ElderRay_H4",

              "ElderRayAlternative_M15",
              "ElderRayAlternative_H1",
              "ElderRayAlternative_H4",

              "ThreeEma_M15",
              "ThreeEma_H1",
              "ThreeEma_H4",

              "ThreeEmaAlternative_M15",
              "ThreeEmaAlternative_H1",
              "ThreeEmaAlternative_H4",

              "EMACrossover_M15",
              "EMACrossover_H1",
              "EMACrossover_H4",

              "EMACrossoverAlternative_M15",
              "EMACrossoverAlternative_H1",
              "EMACrossoverAlternative_H4",

              "EMACrossoverRSI_M15",
              "EMACrossoverRSI_H1",
              "EMACrossoverRSI_H4",

              "EMACrossoverRSIAlternative_M15",
              "EMACrossoverRSIAlternative_H1",
              "EMACrossoverRSIAlternative_H4",

              "EMAMACDRSI_M15",
              "EMAMACDRSI_H1",
              "EMAMACDRSI_H4",

              "EMAMI_M15",
              "EMAMI_H1",
              "EMAMI_H4",

              "ForceIndexEMA_M15",
              "ForceIndexEMA_H1",
              "ForceIndexEMA_H4",

              "KeltnerStochasticAdx_M15",
              "KeltnerStochasticAdx_H1",
              "KeltnerStochasticAdx_H4",

              "KAMA_M15",
              "KAMA_H1",
              "KAMA_H4",

              "KAMACrossover_M15",
              "KAMACrossover_H1",
              "KAMACrossover_H4",

              "KeltnerAdx_M15",
              "KeltnerAdx_H1",
              "KeltnerAdx_H4",

              "KeltnerRsi_M15",
              "KeltnerRsi_H1",
              "KeltnerRsi_H4",

              "KeltnerStochastic_M15",
              "KeltnerStochastic_H1",
              "KeltnerStochastic_H4",

              "MACDCrossover_M15",
              "MACDCrossover_H1",
              "MACDCrossover_H4",

              "MACDHistogramReversal_M15",
              "MACDHistogramReversal_H1",
              "MACDHistogramReversal_H4",

              "MacdRsiSma_M15",
              "MacdRsiSma_H1",
              "MacdRsiSma_H4",

              "MACDStochasticCrossover_M15",
              "MACDStochasticCrossover_H1",
              "MACDStochasticCrossover_H4",

              "MACDZeroCross_M15",
              "MACDZeroCross_H1",
              "MACDZeroCross_H4",

              "MFI_M15",
              "MFI_H1",
              "MFI_H4",

              "OopsSignals_M15",
              "OopsSignals_H1",
              "OopsSignals_H4",

              "PsarMovingAverage_M15",
              "PsarMovingAverage_H1",
              "PsarMovingAverage_H4",

              "Rsi2_M15",
              "Rsi2_H1",
              "Rsi2_H4",

              "Rsi8020_M15",
              "Rsi8020_H1",
              "Rsi8020_H4",

              "SimpleMAExponentialMA_M15",
              "SimpleMAExponentialMA_H1",
              "SimpleMAExponentialMA_H4",

              "SimpleMAExponentialMAAlternative_M15",
              "SimpleMAExponentialMAAlternative_H1",
              "SimpleMAExponentialMAAlternative_H4",

              "SMAMI_M15",
              "SMAMI_H1",
              "SMAMI_H4",

              "StochasticOscillatorNoExit_M15",
              "StochasticOscillatorNoExit_H1",
              "StochasticOscillatorNoExit_H4",

              "TripleBollingerBands_M15",
              "TripleBollingerBands_H1",
              "TripleBollingerBands_H4",

              "TrixEma_M15",
              "TrixEma_H1",
              "TrixEma_H4",

              "TrixMI_M15",
              "TrixMI_H1",
              "TrixMI_H4",

              "TrixRsi_M15",
              "TrixRsi_H1",
              "TrixRsi_H4",

              "TSICrossover_M15",
              "TSICrossover_H1",
              "TSICrossover_H4",

              "VortexCrossover_M15",
              "VortexCrossover_H1",
              "VortexCrossover_H4",

              "VortexSma_M15",
              "VortexSma_H1",
              "VortexSma_H4",

              "WilliamsIndicator_M15",
              "WilliamsIndicator_H1",
              "WilliamsIndicator_H4",

              "WilliamsRsi_M15",
              "WilliamsRsi_H1",
              "WilliamsRsi_H4",

              "WilliamsStochastic_M15",
              "WilliamsStochastic_H1",
              "WilliamsStochastic_H4",

              "ZigZag_M15",
              "ZigZag_H1",
              "ZigZag_H4",

              "EMACrossoverMACD_M15",
              "EMACrossoverMACD_H1",
              "EMACrossoverMACD_H4"]

# does not work
#app.add_middleware(
#    TrustedHostMiddleware, allowed_hosts=["52.89.214.238","34.212.75.30:47464","54.218.53.128","52.32.178.7:58232"]
#)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

class Base(DeclarativeBase):
    pass

class TimeFrame(enum.Enum):
    PERIOD_M1 = 1
    PERIOD_M15 = 15
    PERIOD_H1 = 60
    PERIOD_H4 = 240
    PERIOD_D1 = 6*240
    PERIOD_W1 = 30*6*240

class Regressions(Base):
    __tablename__ = "regressions"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(6))
    timeFrame: Mapped[Enum] = mapped_column(Enum(TimeFrame))
    startTime: Mapped[str] = mapped_column(String(30))
    endTime: Mapped[str] = mapped_column(String(30))
    startValue: Mapped[float]
    endValue: Mapped[float]

    def __repr__(self) -> str:
        return (f"Regression(id={self.id!r}, symbol={self.symbol!r}, timeFrame={self.timeFrame!r}, startTime={self.startTime!r}, endTime={self.endTime!r})"
                f", startValue={self.startValue!r}, endValue={self.endValue!r})")

class IgnoredSignal(Base):
    __tablename__ = "IgnoredSignals"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    json: Mapped[str] = mapped_column(String(64000))
    reason: Mapped[str] = mapped_column(String(64000))

class Signal(Base):
    __tablename__ = "Trades"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(6))
    type: Mapped[str] = mapped_column(String(6))
    entry: Mapped[float]
    sl: Mapped[float]
    tp: Mapped[float]
    lots: Mapped[float]
    spread: Mapped[float] = mapped_column(nullable=True, default=0.0)
    tradeid: Mapped[int] = mapped_column(nullable=True, default=0)
    stamp: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    # werden erst nach der Erstellung des Trades gesetzt
    activated: Mapped[str] = mapped_column(nullable=True, default="")
    openprice: Mapped[float] = mapped_column(nullable=True, default=0.0)
    swap: Mapped[float] = mapped_column(nullable=True, default=0.0)
    profit: Mapped[float] = mapped_column(nullable=True, default=0.0)
    closed: Mapped[str] = mapped_column(nullable=True, default="")
    commision: Mapped[float] = mapped_column(nullable=True, default="")
    strategy: Mapped[str] = mapped_column(nullable=True, default="")

class ProdSignal(Base):
    __tablename__ = "ProdTrades"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(6))
    type: Mapped[str] = mapped_column(String(6))
    entry: Mapped[float]
    sl: Mapped[float]
    tp: Mapped[float]
    lots: Mapped[float]
    spread: Mapped[float] = mapped_column(nullable=True, default=0.0)
    tradeid: Mapped[int] = mapped_column(nullable=True, default=0)
    stamp: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    # werden erst nach der Erstellung des Trades gesetzt
    activated: Mapped[str] = mapped_column(nullable=True, default="")
    openprice: Mapped[float] = mapped_column(nullable=True, default=0.0)
    swap: Mapped[float] = mapped_column(nullable=True, default=0.0)
    profit: Mapped[float] = mapped_column(nullable=True, default=0.0)
    closed: Mapped[str] = mapped_column(nullable=True, default="")
    commision: Mapped[float] = mapped_column(nullable=True, default="")
    strategy: Mapped[str] = mapped_column(nullable=True, default="")

class CandlesEntity(Base):
    __tablename__ = "Candles"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    SYMBOL: Mapped[str] = mapped_column(String(6))
    TIMEFRAME: Mapped[Enum] = mapped_column(Enum(TimeFrame))
    DATETIME: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    ##TIMESTAMP:Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    OPEN: Mapped[float]
    HIGH: Mapped[float]
    LOW: Mapped[float]
    CLOSE: Mapped[float]
    TICKVOL: Mapped[float]
    VOL: Mapped[float]
    SPREAD: Mapped[float]
    UniqueConstraint("SYMBOL", "TIMEFRAME", "DATETIME", "OPEN", "CLOSE", name="uix_1")
    #STAMP: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())

    def __repr__(self) -> str:
        return (f"Candles(id={self.id!r}, DATETIME={self.DATETIME!r}"
                f", OPEN={self.OPEN!r}, CLOSE={self.CLOSE!r})")

class TrendInfoEntity(Base):
    __tablename__ = "TrendInfo"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(6))
    stamp: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    trendscore:Mapped[int]
    uptrend:Mapped[bool]
    r1: Mapped[float]
    s1: Mapped[float]


class SignalDto(BaseModel):
    symbol:str
    timestamp:str
    type:str
    entry:float
    sl:float
    tp:float
    strategy: str

class TrendInfoDto(BaseModel):
    symbol:str
    timestamp:str
    trendScore:int
    uptrend:bool
    r1: float
    s1: float
    strategy: str

def getSignalStats(strategy:str, symbol:str, session):
        signalStats = session.query(Signal.strategy,
                                    func.count(Signal.id).filter(Signal.profit != 0).label("alltrades"),
                                    func.count(Signal.id).filter(Signal.profit < 0).label("failedtrades"),
                                    func.count(Signal.id).filter(Signal.profit > 0).label("successtrades"),
                                    func.sum(Signal.profit).label("profit")).filter(Signal.strategy == strategy, Signal.symbol == symbol).group_by(Signal.strategy).first()
        session.expunge_all()
        return signalStats

def wwma(values, n):
    """
     J. Welles Wilder's EMA
    """
    return values.ewm(alpha=1/n, adjust=False).mean()

def atr(df, n=14):
    data = df.copy()
    high = data['HIGH']
    low = data['LOW']
    close = data['CLOSE']
    data['tr0'] = abs(high - low)
    data['tr1'] = abs(high - close.shift())
    data['tr2'] = abs(low - close.shift())
    tr = data[['tr0', 'tr1', 'tr2']].max(axis=1)
    atr = wwma(tr, n)
    return atr

def loadDfFromDb(symbol:str, timeFrame:TimeFrame, session, limit=250000):

    df = pd.read_sql_query(
        sql = session.query(CandlesEntity.SYMBOL,
                            CandlesEntity.TIMEFRAME,
                            CandlesEntity.DATETIME,
                            CandlesEntity.OPEN,
                            CandlesEntity.HIGH,
                            CandlesEntity.LOW,
                            CandlesEntity.CLOSE,
                            CandlesEntity.TICKVOL,
                            CandlesEntity.VOL,
                            CandlesEntity.SPREAD)
        .filter(CandlesEntity.SYMBOL == symbol, CandlesEntity.TIMEFRAME == timeFrame)
        .order_by(CandlesEntity.id.desc())
        .limit(limit)
        .statement,
        con = engine
    )
    #print(len(df), " database entries loaded for ",timeFrame)
    #print("Last row: ")
    #print(df.iloc[-1])
    df_no_duplicates = df.drop_duplicates(subset=['DATETIME'])
    return df_no_duplicates.drop_duplicates()

def lastCandle(symbol:str, timeFrame:TimeFrame):
    with Session.begin() as session:
        candle = session.query(CandlesEntity).filter(CandlesEntity.SYMBOL == symbol, CandlesEntity.TIMEFRAME == timeFrame).order_by(CandlesEntity.DATETIME.desc()).first()
        session.expunge(candle)
        session.close()
        return candle

#@app.get("/atr/")
#async def atrEndpoint(symbol:str, timeframe: str):
#    timeframeEnum: TimeFrame = TimeFrame.__dict__[timeframe]

    #df = loadDfFromDb(symbol, timeframeEnum)
    #atrValue = atr(df)
    #x = df.iloc[-1].CLOSE - atrValue.iloc[-1]
    #y  = df.iloc[-1].CLOSE + atrValue.iloc[-1]
    #return {'atr:': atrValue.iloc[-1],
    #        'lastprice': df.iloc[-1].CLOSE,
    #        'lastprice-atr': x,
    #        'lastprice+atr': y}


@app.post("/resendsignal/")
async def resendsignal(
        id: Annotated[int, Form()],
        symbol: Annotated[str, Form()],
        timestamp: Annotated[str, Form()],
        type: Annotated[str, Form()],
        entry: Annotated[float, Form()],
        sl: Annotated[float, Form()],
        tp: Annotated[float, Form()],
        strategy: Annotated[str, Form()]):

    signal = SignalDto(
        symbol=symbol,
        timestamp= timestamp,
        type = type,
        entry = entry,
        sl = sl,
        tp = tp,
        strategy = strategy
    )
    proceedSignal(signal)

    with Session.begin() as session:
        # TODO delete IgnoredSignal when comes here
        signal = session.query(IgnoredSignal).filter(IgnoredSignal.id == id).first()
        if signal is not None:
            session.delete(signal)
            session.commit()
            session.close()

@app.post("/trendinfo")
async def signals(trendInfo:TrendInfoDto):
    print("########################################trendinfo########################################")
    print(str(trendInfo))
    print("########################################trendinfo########################################")
    #proceedSignal(signal)
    with Session.begin() as session:
        storedInfo = session.query(TrendInfoEntity).filter(TrendInfoEntity.symbol == trendInfo.symbol).first()
        if storedInfo is not None:
            session.delete(storedInfo)
        info = TrendInfoEntity(
            symbol=trendInfo.symbol,
            trendscore=trendInfo.trendScore,
            uptrend=trendInfo.uptrend,
            r1=trendInfo.r1,
            s1=trendInfo.s1
        )
        session.add(info)
        session.commit()
        session.close()

@app.post("/signal")
async def signals(signal:SignalDto):
    proceedSignal(signal)

def storeProdSignal(signal: ProdSignal, session):
    session.add(signal)
    session.commit()

def storeSignal(signal: Signal, session):
    session.add(signal)
    session.commit()

def storeIgnoredSignal(signal: IgnoredSignal, session):
    session.add(signal)
    session.commit()


def calculateSlAndStoreSignal(signal, strategy, jsonSignal, session):
    df = loadDfFromDb(signal.symbol, TimeFrame.PERIOD_H4, session, 10000)
    atrValue = atr(df)

    sl = 0.0
    tp = 0.0
    if signal.type == "sell":
        sl = signal.entry + atrValue.iloc[-1]
        tp = signal.entry - atrValue.iloc[-1]
    if signal.type == "buy":
        sl = signal.entry - atrValue.iloc[-1]
        tp = signal.entry + atrValue.iloc[-1]

    lots = 0.1
    signalStats = getSignalStats(strategy, signal.symbol, session)

    if signalStats is None:
        lots = 0.01
    elif signalStats.failedtrades > signalStats.successtrades:
        lots = 0.01

    if signalStats is not None and signalStats.alltrades > 100:
        percentage = (100 / signalStats.alltrades) * signalStats.successtrades
        if percentage < 58:
            storeIgnoredSignal(IgnoredSignal(
                json=jsonSignal,
                reason=f"Ignored, because it has {signalStats.failedtrades} failed Trades (All: {signalStats.alltrades}, Sucess: {signalStats.successtrades}) and Win-Percentage is {percentage}!"
            ), session)
            session.close()
            return
        else:
            prodSignalsCount = session.query(ProdSignal).filter(ProdSignal.activated == "", ProdSignal.openprice == 0.0).count()
            if prodSignalsCount <= 5 and signalStats.profit > 1:
                storeProdSignal(ProdSignal(
                    symbol=signal.symbol,
                    type=signal.type,
                    entry=signal.entry,
                    sl=sl,
                    tp=tp,
                    lots=0.01,
                    commision=0.0,
                    strategy=strategy
                ), session)

    storeSignal(Signal(
        symbol=signal.symbol,
        type=signal.type,
        entry=signal.entry,
        sl=sl,
        tp=tp,
        lots=lots,
        commision=0.0,
        strategy=strategy
    ), session)



def proceedSignal(signal):
    # no need to check for trend in TradingView we send everything
    # and do the check here
    # D-EMA200, H4-EMA, D-Regression, H4-Regression
    # Support Resistance

    #ignored XRPUSD
    if signal.symbol == "XRPUSD":
        return

    strategy = signal.strategy.replace("GaussianChannelTrendAi", "GaussianChannelTrendAI")
    strategy = strategy.replace("T3-machineLearningLogisticRegression","T3-MachineLearningLogisticRegression")
    jsonSignal =str({'symbol': signal.symbol,
                     'timestamp': signal.timestamp,
                     'type': signal.type,
                     'entry': signal.entry,
                     'sl': signal.sl,
                     'tp': signal.tp,
                     'strategy': strategy})

    with Session.begin() as session:

        if signal.symbol not in symbols:
            #print(f"Ignore Signal because symbol is not handled yet: {signal}")
            storeIgnoredSignal(IgnoredSignal(
                json=jsonSignal,
                reason=f"Ignore Signal because symbol is not handled yet: {signal}"
            ),session)
            session.close()
            return

        if strategy not in strategies:
            #print(f"Ignore Signal because strategy is unknown: {strategy}")
            storeIgnoredSignal(IgnoredSignal(
                json=jsonSignal,
                reason=f"Ignore Signal because strategy is unknown: {strategy}"
            ),session)
            session.close()
            return

        trendInfo = session.query(TrendInfoEntity).filter(TrendInfoEntity.symbol == signal.symbol).first()
        if trendInfo is not None:
            if trendInfo.trendscore > -7 and signal.type == "sell":
                #print(f"Ignore Signal because signal {signal} is against trendscore: {trendInfo.trendscore} \n")
                #if trendInfo.trendscore == -6:
                #    storeIgnoredSignal(IgnoredSignal(
                #        json=jsonSignal,
                #        reason=f"Ignore Signal because signal {signal} is against trendscore: {trendInfo.trendscore}"
                #    ),session)
                session.close()
                return
            if trendInfo.trendscore < 7 and signal.type == "buy":
                #print(f"Ignore Signal because signal {signal} is against trendscore: {trendInfo.trendscore} \n")
                #if trendInfo.trendscore == 6:
                #    storeIgnoredSignal(IgnoredSignal(
                #        json=jsonSignal,
                #        reason=f"Ignore Signal because signal {signal} is against trendscore: {trendInfo.trendscore}"
                #    ),session)
                session.close()
                return
        if trendInfo is None:
            print(f"Ignore Signal {signal} because TrendInfo not found!")
            storeIgnoredSignal(IgnoredSignal(
                json=jsonSignal,
                reason=f"Ignore Signal {signal} because TrendInfo not found!"
            ),session)
            session.close()
            return

        #print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        #print("++++++++++++++++++++++++FIRST CHECKS PASSED++++++++++++++++++++++++")
        #print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

        if strategy == "VHMA" or strategy == "RSS_WMA" or strategy == "Super AI Trend" or strategy == "SSL Hybrid" or strategy == "SentimentRangeMa" or strategy == "T3-EmaStrategy" or strategy == "T3-AroonBased":
            calculateSlAndStoreSignal(signal, strategy + "_WITHOUT_REG", jsonSignal, session)


        regressionLineH4 = session.query(Regressions).filter(
            Regressions.symbol == signal.symbol, Regressions.timeFrame == TimeFrame.PERIOD_H4).all()

        if len(regressionLineH4) > 0:

            if "buy" == signal.type and signal.entry < regressionLineH4[0].endValue:
                print(f"Ignore (2. Condition) Buy-Signal: {signal}, Regression-End: {regressionLineH4[0].endValue}")
                #storeIgnoredSignal(IgnoredSignal(
                #    json=jsonSignal,
                #    reason=f"Ignore (2. Condition) Buy-Signal: {signal.entry}, Regression-End: {regressionLineH4[0].endValue}"
                #))
                session.close()
                return

            if "sell" == signal.type and signal.entry > regressionLineH4[0].endValue:
                print(f"Ignore (2. Condition) Sell-Signal: {signal}, Regression-End: {regressionLineH4[0].endValue}")
                #storeIgnoredSignal(IgnoredSignal(
                #    json=jsonSignal,
                #    reason=f"Ignore (2. Condition) Sell-Signal: {signal.entry}, Regression-End: {regressionLineH4[0].endValue}"
                #))
                session.close()
                return

            calculateSlAndStoreSignal(signal, strategy, jsonSignal, session)
            session.close()
            print(f"######## {signal} stored ########")
        else:
            regressionLineD1 = session.query(Regressions).filter(
                Regressions.symbol == signal.symbol, Regressions.timeFrame == TimeFrame.PERIOD_D1).all()
            if len(regressionLineD1) > 0:
                if "buy" == signal.type and signal.entry < regressionLineD1[0].endValue:
                    print(f"Ignore (2. Condition) Buy-Signal: {signal}, Regression-End: {regressionLineD1[0].endValue}")
                    #storeIgnoredSignal(IgnoredSignal(
                    #    json=jsonSignal,
                    #    reason=f"Ignore (2. Condition) Buy-Signal: {signal.entry}, Regression-End: {regressionLineD1[0].endValue}"
                    #))
                    return

                if "sell" == signal.type and signal.entry > regressionLineD1[0].endValue:
                    print(f"Ignore (2. Condition) Sell-Signal: {signal}, Regression-End: {regressionLineD1[0].endValue}")
                    #storeIgnoredSignal(IgnoredSignal(
                    #    json=jsonSignal,
                    #    reason=f"Ignore (2. Condition) Sell-Signal: {signal.entry}, Regression-End: {regressionLineD1[0].endValue}"
                    #))
                    return

                df = loadDfFromDb(signal.symbol, TimeFrame.PERIOD_D1, session)
                atrValue = atr(df)

                sl = 0.0
                tp = 0.0
                if signal.type == "sell":
                    sl = signal.entry + atrValue.iloc[-1]
                    tp = signal.entry - atrValue.iloc[-1]
                if signal.type == "buy":
                    sl = signal.entry - atrValue.iloc[-1]
                    tp = signal.entry + atrValue.iloc[-1]

                storeSignal(Signal(
                    symbol=signal.symbol,
                    type=signal.type,
                    entry=signal.entry,
                    sl=sl,
                    tp=tp,
                    lots=0.1,
                    commision=0.0,
                    strategy=strategy
                ), session)
                print(f"######## {signal} stored ########")
                session.close()
            else:
                print(f"No Regression-Data found for {signal.symbol}")

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    #port can only be 80 see tradingview
    uvicorn.run(app, host="0.0.0.0", port=80)