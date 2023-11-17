import pandas as pd
from fastapi import FastAPI, Request, status, Form
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.trustedhost import TrustedHostMiddleware
# Bellow the import create a job that will be executed on background
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import String
from sqlalchemy import create_engine, DateTime, func
from sqlalchemy import String, Enum, DateTime, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Enum
import enum
import uvicorn
from typing_extensions import Annotated
from dotenv import load_dotenv
import os

load_dotenv()

#engine = create_engine('postgresql://nobodysforex:pwd@db:6432/trading-db')
engine = create_engine(os.environ['POSTGRES_URL'])
Session = sessionmaker(bind=engine)
session = Session()

app = FastAPI()

symbols = ["AUDUSD", "AUDCHF", "AUDJPY", "AUDNZD", "CHFJPY", "EURUSD", "EURCHF", "EURNZD", "GBPUSD", "GBPCAD", "GBPCHF", "GBPNZD",  "XAGUSD", "USDCAD", "USDCHF", "XRPUSD"]
strategies = ["NNR", "Super AI Trend", "70% Strategy", "SSL Hybrid", "AI Volume Supertrend", "SSL + Wave Trend Strategy", "VHMA", "T3Fvma", "SentimentRangeMa"]

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

#@app.get("/")
#async def read_root():
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

def loadDfFromDb(symbol:str, timeFrame:TimeFrame):
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
    return session.query(CandlesEntity).filter(CandlesEntity.SYMBOL == symbol, CandlesEntity.TIMEFRAME == timeFrame).order_by(CandlesEntity.DATETIME.desc()).first()

@app.get("/atr/")
async def atrEndpoint(symbol:str, timeframe: str):
    timeframeEnum: TimeFrame = TimeFrame.__dict__[timeframe]

    df = loadDfFromDb(symbol, timeframeEnum)
    atrValue = atr(df)
    x = df.iloc[-1].CLOSE - atrValue.iloc[-1]
    y  = df.iloc[-1].CLOSE + atrValue.iloc[-1]
    return {'atr:': atrValue.iloc[-1],
            'lastprice': df.iloc[-1].CLOSE,
            'lastprice-atr': x,
            'lastprice+atr': y}


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
    # TODO delete IgnoredSignal when comes here
    signal = session.query(IgnoredSignal).filter(IgnoredSignal.id == id).first()
    if signal is not None:
        session.delete(signal)
        session.commit()

@app.post("/signal")
async def signals(signal:SignalDto):
    proceedSignal(signal)

def storeSignal(signal: Signal):
    session.add(signal)
    session.commit()

def storeIgnoredSignal(signal: IgnoredSignal):
    session.add(signal)
    session.commit()

def proceedSignal(signal):
    # no need to check for trend in TradingView we send everything
    # and do the check here
    # D-EMA200, H4-EMA, D-Regression, H4-Regression
    # Support Resistance

    jsonSignal =str({'symbol': signal.symbol,
                     'timestamp': signal.timestamp,
                     'type': signal.type,
                     'entry': signal.entry,
                     'sl': signal.sl,
                     'tp': signal.tp,
                     'strategy': signal.strategy})

    if signal.symbol not in symbols:
        print(f"Ignore Signal because symbol is not handled yet: {signal}")
        storeIgnoredSignal(IgnoredSignal(
            json=jsonSignal,
            reason=f"Ignore Signal because symbol is not handled yet: {signal}"
        ))
        return

    if signal.strategy not in strategies:
        print(f"Ignore Signal because strategy is unknown: {signal.strategy}")
        storeIgnoredSignal(IgnoredSignal(
            json=jsonSignal,
            reason=f"Ignore Signal because strategy is unknown: {signal.strategy}"
        ))
        return

    #because of setting sl and tp here we can not check it here anymore
    #if "buy" == signal.type and signal.sl > signal.tp:
    #    print(f"Ignore (1. Condition) Buy-Signal: {signal}")
    #    storeIgnoredSignal(IgnoredSignal(
    #        json=jsonSignal,
    #        reason=f"Ignore (1. Condition) Buy-Signal: {signal}"
    #    ))
    #    return

    #if "sell" == signal.type and signal.sl < signal.tp:
    #    print(f"Ignore (1. Condition) Sell-Signal: {signal}")
    #    storeIgnoredSignal(IgnoredSignal(
    #        json=jsonSignal,
    #        reason=f"Ignore (1. Condition) Sell-Signal: {signal}"
    #    ))
    #    return

    regressionLineD1 = Session().query(Regressions).filter(
        Regressions.symbol == signal.symbol, Regressions.timeFrame == TimeFrame.PERIOD_D1).all()

    regressionLineH4 = Session().query(Regressions).filter(
        Regressions.symbol == signal.symbol, Regressions.timeFrame == TimeFrame.PERIOD_H4).all()

    if len(regressionLineH4) > 0:

        if "buy" == signal.type and signal.entry < regressionLineH4[0].endValue:
            print(f"Ignore (2. Condition) Buy-Signal: {signal}, Regression-End: {regressionLineH4[0].endValue}")
            storeIgnoredSignal(IgnoredSignal(
                json=jsonSignal,
                reason=f"Ignore (2. Condition) Buy-Signal: {signal.entry}, Regression-End: {regressionLineH4[0].endValue}"
            ))
            return

        if "sell" == signal.type and signal.entry > regressionLineH4[0].endValue:
            print(f"Ignore (2. Condition) Sell-Signal: {signal}, Regression-End: {regressionLineH4[0].endValue}")
            storeIgnoredSignal(IgnoredSignal(
                json=jsonSignal,
                reason=f"Ignore (2. Condition) Sell-Signal: {signal.entry}, Regression-End: {regressionLineH4[0].endValue}"
            ))
            return

        df = loadDfFromDb(signal.symbol, TimeFrame.PERIOD_H4)
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
            strategy=signal.strategy
        ))
    elif len(regressionLineD1) > 0:
        if "buy" == signal.type and signal.entry < regressionLineD1[0].endValue:
            print(f"Ignore (2. Condition) Buy-Signal: {signal}, Regression-End: {regressionLineD1[0].endValue}")
            storeIgnoredSignal(IgnoredSignal(
                json=jsonSignal,
                reason=f"Ignore (2. Condition) Buy-Signal: {signal.entry}, Regression-End: {regressionLineD1[0].endValue}"
            ))
            return

        if "sell" == signal.type and signal.entry > regressionLineD1[0].endValue:
            print(f"Ignore (2. Condition) Sell-Signal: {signal}, Regression-End: {regressionLineD1[0].endValue}")
            storeIgnoredSignal(IgnoredSignal(
                json=jsonSignal,
                reason=f"Ignore (2. Condition) Sell-Signal: {signal.entry}, Regression-End: {regressionLineD1[0].endValue}"
            ))
            return

        df = loadDfFromDb(signal.symbol, TimeFrame.PERIOD_H4)
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
            strategy=signal.strategy
        ))
    else:
        print(f"No Regression-Data found for {signal.symbol}")

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    #port can only be 80 see tradingview
    uvicorn.run(app, host="0.0.0.0", port=80)