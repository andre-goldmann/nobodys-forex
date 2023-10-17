import json

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.trustedhost import TrustedHostMiddleware
# Bellow the import create a job that will be executed on background
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import String
from sqlalchemy import create_engine, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Enum
import enum

engine = create_engine('postgresql://nobodysforex:pwd@db:6432/trading-db')
Session = sessionmaker(bind=engine)
session = Session()

app = FastAPI()

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
    __tablename__ = "IgnoredSignal"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    json: Mapped[str] = mapped_column(String(64000))
    reason: Mapped[str] = mapped_column(String(64000))

class Trade(Base):
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

class SignalDto(BaseModel):
    symbol:str
    timestamp:str
    type:str
    entry:float
    sl:float
    tp:float
    strategy: str

@app.get("/")
async def read_root():
    message = f"Hello world!"
    return {"message": message}

@app.post("/signal")
async def signals(signal:SignalDto):
    print(signal)

    # no need to check for trend in TradingView we send everything
    # and do the check here
    # D-EMA200, H4-EMA, D-Regression, H4-Regression
    # Support Resistance

    if "buy" == signal.type and signal.sl > signal.tp:
        print(f"Ignore (1. Condition) Buy-Signal: {signal}")
        storeIgnoredSignal(IgnoredSignal(
            json=json.dumps(signal),
            reason=f"Ignore (1. Condition) Buy-Signal: {signal}"
        ))
        return

    if "sell" == signal.type and signal.sl < signal.tp:
        print(f"Ignore (1. Condition) Sell-Signal: {signal}")
        storeIgnoredSignal(IgnoredSignal(
            json=json.dumps(signal),
            reason=f"Ignore (1. Condition) Sell-Signal: {signal}"
        ))
        return

    regressionLineD1 = Session().query(Regressions).filter(
        Regressions.symbol == signal.symbol, Regressions.timeFrame == TimeFrame.PERIOD_D1).all()

    regressionLineH4 = Session().query(Regressions).filter(
        Regressions.symbol == signal.symbol, Regressions.timeFrame == TimeFrame.PERIOD_H4).all()

    if len(regressionLineH4) > 0:

        if "buy" == signal.type and signal.entry < regressionLineH4[0].endValue:
            print(f"Ignore (2. Condition) Buy-Signal: {signal}, Regression-End: {regressionLineH4[0].endValue}")
            storeIgnoredSignal(IgnoredSignal(
                json=json.dumps(signal),
                reason=f"Ignore (2. Condition) Buy-Signal: {signal}, Regression-End: {regressionLineH4[0].endValue}"
            ))
            return

        if "sell" == signal.type and signal.entry > regressionLineH4[0].endValue:
            print(f"Ignore (2. Condition) Sell-Signal: {signal}, Regression-End: {regressionLineH4[0].endValue}")
            storeIgnoredSignal(IgnoredSignal(
                json=json.dumps(signal),
                reason=f"Ignore (2. Condition) Sell-Signal: {signal}, Regression-End: {regressionLineH4[0].endValue}"
            ))
            return

        storeTrade(Trade(
            symbol=signal.symbol,
            type=signal.type,
            entry=signal.entry,
            sl=signal.sl,
            tp=signal.tp,
            lots=0.5,
            commision=0.0,
            strategy=signal.strategy
        ))
    elif len(regressionLineD1) > 0:
        if "buy" == signal.type and signal.entry < regressionLineD1[0].endValue:
            print(f"Ignore (2. Condition) Buy-Signal: {signal}, Regression-End: {regressionLineD1[0].endValue}")
            storeIgnoredSignal(IgnoredSignal(
                json=json.dumps(signal),
                reason=f"Ignore (2. Condition) Buy-Signal: {signal}, Regression-End: {regressionLineD1[0].endValue}"
            ))
            return

        if "sell" == signal.type and signal.entry > regressionLineD1[0].endValue:
            print(f"Ignore (2. Condition) Sell-Signal: {signal}, Regression-End: {regressionLineD1[0].endValue}")
            storeIgnoredSignal(IgnoredSignal(
                json=json.dumps(signal),
                reason=f"Ignore (2. Condition) Sell-Signal: {signal}, Regression-End: {regressionLineD1[0].endValue}"
            ))
            return

        storeTrade(Trade(
            symbol=signal.symbol,
            type=signal.type,
            entry=signal.entry,
            sl=signal.sl,
            tp=signal.tp,
            lots=0.1,
            commision=0.0,
            strategy=signal.strategy
        ))
    else:
        print(f"No Regression-Data found for {signal.symbol}")

@app.post("/ignoredsignals")
async def signals():
    signals = session.query(IgnoredSignal.id,
                            IgnoredSignal.json,
                            IgnoredSignal.reason).all()
    result = []
    print("###################################")
    print(f"IgnoredSignals from db loaded:{len(signals)}")
    print("###################################")
    for signal in signals:
        result.append({'id': signal.id,
                       'json': signal.json,
                       'reason': signal.reason})

    return result


def storeTrade(trade: Trade):
    session.add(trade)
    session.commit()

def storeIgnoredSignal(signal: IgnoredSignal):
    session.add(signal)
    session.commit()

#if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=80)