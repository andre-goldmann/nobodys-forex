import enum

from pydantic import BaseModel
from sqlalchemy import String
from sqlalchemy import create_engine, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import sessionmaker


# Docker-Config
engine = create_engine('postgresql://nobodysforex:pwd@db:6432/trading-db')
Session = sessionmaker(bind=engine)
session = Session()

symbols = ["AUDUSD", "AUDCHF", "AUDJPY", "AUDNZD", "CHFJPY", "EURUSD", "EURCHF", "EURNZD", "GBPUSD", "GBPCAD", "GBPCHF", "GBPNZD",  "XAGUSD", "USDCAD", "USDCHF", "XRPUSD"]
tradeTypes = ["buy", "sell"]

class TimeFrame(enum.Enum):
    PERIOD_M1 = 1
    PERIOD_M15 = 15
    PERIOD_H1 = 60
    PERIOD_H4 = 240
    PERIOD_D1 = 6*240
    PERIOD_W1 = 30*6*240

class Base(DeclarativeBase):
    pass

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
    activated: Mapped[str] = mapped_column(nullable=True, default="")
    openprice: Mapped[float] = mapped_column(nullable=True, default=0.0)
    swap: Mapped[float] = mapped_column(nullable=True, default=0.0)
    profit: Mapped[float] = mapped_column(nullable=True, default=0.0)
    closed: Mapped[str] = mapped_column(nullable=True, default="")
    commision: Mapped[float] = mapped_column(nullable=True, default=0.0)
    strategy: Mapped[str] = mapped_column(nullable=True, default="")

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class SignalActivationDto(BaseModel):
    symbol:str
    timestamp:str
    magic:int
    open_price:float

class SignalUpdateDto(BaseModel):
    symbol:str
    timestamp:str
    magic:int
    profit: float
    swap:float
    closed:str
    commision:float

class HistoryUpdateDto(BaseModel):
    symbol:str
    closed:str
    magic:int
    profit: float
    swap:float
    commision:float

def storeSignal(signal: Signal):
    session.add(signal)
    session.commit()

def modifySignalInDb(id:int, type:str, entry:float, sl:float, tp:float, lots:float):
    storeSignal = session.query(Signal).filter(Signal.id == id).first()
    if storeSignal is not None:
        storeSignal.type=type
        storeSignal.entry=entry
        storeSignal.sl=sl
        storeSignal.tp=tp
        storeSignal.lots=lots
        session.commit()

def deleteSignalInDb(id:int):
    storeSignal = session.query(Signal).filter(Signal.id == id).first()
    if storeSignal is not None:
        session.delete(storeSignal)
        session.commit()

def getWaitingSignals():
    return session.query(Signal.id,
                         Signal.symbol,
                         Signal.type,
                         Signal.entry,
                         Signal.sl,
                         Signal.tp,
                         Signal.lots,
                         Signal.stamp).filter(Signal.tradeid == 0, Signal.activated == "", Signal.openprice == 0.0).all()

def getExecutedSignals():
    return session.query(Signal.id,
                         Signal.symbol,
                         Signal.type,
                         Signal.entry,
                         Signal.sl,
                         Signal.tp,
                         Signal.lots,
                         Signal.stamp,
                         Signal.strategy,
                         Signal.activated,
                         Signal.openprice,
                         Signal.profit,
                         Signal.commision,
                         Signal.swap,
                         Signal.closed).filter(Signal.openprice > 0.0).all()

def signalStats():
    return session.query(Signal.symbol,Signal.strategy, func.sum(Signal.profit), func.sum(Signal.swap)).group_by(Signal.symbol, Signal.strategy).all()

def activateSignal(tradeActivationDto:SignalActivationDto):
    #print("Activating Trade", tradeActivationDto)

    storeSignal = session.query(Signal).filter(Signal.symbol == tradeActivationDto.symbol, Signal.id == tradeActivationDto.magic).first()
    storeSignal.activated=tradeActivationDto.timestamp
    storeSignal.openprice=tradeActivationDto.open_price
    session.commit()
    #print("Trade Activated:", storeSignal.openprice)

def updateSignalInDb(signalUpdateDto:SignalUpdateDto):
    #print("Updating Trade", tradeUpdateDto)

    storedSignal = session.query(Signal).filter(Signal.symbol == signalUpdateDto.symbol, Signal.id == signalUpdateDto.magic).first()
    if storedSignal is not None:
        storedSignal.swap = signalUpdateDto.swap
        storedSignal.profit = signalUpdateDto.profit
        storedSignal.commision = signalUpdateDto.commision
        if signalUpdateDto.closed is not None and signalUpdateDto.closed != "" and signalUpdateDto.closed != "-":
            storedSignal.closed = signalUpdateDto.closed

        session.commit()
    #print("Trade Updated:", storedSignal)

def updateSignalByHistory(historyUpdateDto:HistoryUpdateDto):
    #print("Updating Trade", tradeUpdateDto)
    print(historyUpdateDto)
    storedSignal = session.query(Signal).filter(Signal.symbol == historyUpdateDto.symbol, Signal.id == historyUpdateDto.magic).first()
    if storedSignal is not None:
        storedSignal.swap = historyUpdateDto.swap
        storedSignal.profit = historyUpdateDto.profit
        storedSignal.commision = historyUpdateDto.commision
        if historyUpdateDto.closed is not None and historyUpdateDto.closed != "" and historyUpdateDto.closed != "-":
            storedSignal.closed = historyUpdateDto.closed

        session.commit()
        print("Updated...")
    else:
        print("Not found...")

def initTradingDb():
    #Trade.__table__.drop(engine)
    Base.metadata.create_all(engine)