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
              "70% Strategy",
              "SSL Hybrid",
              "AI Volume Supertrend",
              "SSL + Wave Trend Strategy",
              "VHMA",
              "T3Fvma",
              "SentimentRangeMa",
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
              "T3-EmaStrategy",
              "SOTT-Lorentzian"]

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

class SignalDto(BaseModel):
    symbol:str
    timestamp:str
    type:str
    entry:float
    sl:float
    tp:float
    strategy: str

def getSignalStats(strategy:str, symbol:str):
    with Session.begin() as session:
        signalStats = session.query(Signal.strategy,
                                    func.count(Signal.id).label("alltrades"),
                                    func.count(Signal.id).filter(Signal.profit < 0).label("failedtrades"),
                                    func.count(Signal.id).filter(Signal.profit > 0).label("successtrades"),
                                    func.sum(Signal.profit).label("profit")).filter(Signal.strategy == strategy, Signal.symbol == symbol).group_by(Signal.strategy).first()
        session.expunge_all()
        session.close()
        return signalStats

#@app.get("/")
#async def read_root(strategy:str):
#    signalStats = getSignalStats(strategy)
#    print("strategystats")
#    print(signalStats.profit)
#    print(signalStats.failedtrades)
#    print(signalStats.successtrades)
#    message = f"Hello world!"
#    return {"message": message}

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

def loadDfFromDb(symbol:str, timeFrame:TimeFrame, session):

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
        .statement,
        con = engine
    )
    print(len(df), " database entries loaded for ",timeFrame)
    #print("Last row: ")
    #print(df.iloc[-1])
    return df

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

def proceedSignal(signal):
    # no need to check for trend in TradingView we send everything
    # and do the check here
    # D-EMA200, H4-EMA, D-Regression, H4-Regression
    # Support Resistance
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
            print(f"Ignore Signal because symbol is not handled yet: {signal}")
            storeIgnoredSignal(IgnoredSignal(
                json=jsonSignal,
                reason=f"Ignore Signal because symbol is not handled yet: {signal}"
            ),session)
            session.close()
            return

        if strategy not in strategies:
            print(f"Ignore Signal because strategy is unknown: {strategy}")
            storeIgnoredSignal(IgnoredSignal(
                json=jsonSignal,
                reason=f"Ignore Signal because strategy is unknown: {strategy}"
            ),session)
            session.close()
            return

        regressionLineH4 = session.query(Regressions).filter(
            Regressions.symbol == signal.symbol, Regressions.timeFrame == TimeFrame.PERIOD_H4).all()

        if len(regressionLineH4) > 0:

            if "buy" == signal.type and signal.entry < regressionLineH4[0].endValue:
                print(f"Ignore (2. Condition) Buy-Signal: {signal}, Regression-End: {regressionLineH4[0].endValue}")
                #storeIgnoredSignal(IgnoredSignal(
                #    json=jsonSignal,
                #    reason=f"Ignore (2. Condition) Buy-Signal: {signal.entry}, Regression-End: {regressionLineH4[0].endValue}"
                #))
                return

            if "sell" == signal.type and signal.entry > regressionLineH4[0].endValue:
                print(f"Ignore (2. Condition) Sell-Signal: {signal}, Regression-End: {regressionLineH4[0].endValue}")
                #storeIgnoredSignal(IgnoredSignal(
                #    json=jsonSignal,
                #    reason=f"Ignore (2. Condition) Sell-Signal: {signal.entry}, Regression-End: {regressionLineH4[0].endValue}"
                #))
                return

            df = loadDfFromDb(signal.symbol, TimeFrame.PERIOD_H4, session)
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
            signalStats = getSignalStats(strategy, signal.symbol)
            #print(signalStats.profit)
            #print(signalStats.failedtrades)
            #print(signalStats.successtrades)
            if signalStats is None:
                lots = 0.01
            elif signalStats.failedtrades > signalStats.successtrades:
                lots = 0.01

            if signalStats.alltrades > 100:
                percentage = (100 / signalStats.alltrades) * signalStats.successtrades
                if percentage < 0.55:
                    storeIgnoredSignal(IgnoredSignal(
                        json=jsonSignal,
                        reason=f"Signal {signal} ignored, because it has more {signalStats.failedtrades} failed Trades and Win-Percentage is {percentage}!"

                    ), session)
                    return
                else:
                    prodSignalsCount = session.query(ProdSignal).filter(ProdSignal.tradeid == 0, ProdSignal.activated == "", ProdSignal.openprice == 0.0).count()
                    if prodSignalsCount <= 5:
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
            session.close()
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
                session.close()
            else:
                print(f"No Regression-Data found for {signal.symbol}")

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    #port can only be 80 see tradingview
    uvicorn.run(app, host="0.0.0.0", port=80)