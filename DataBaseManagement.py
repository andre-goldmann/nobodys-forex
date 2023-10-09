import enum

from pydantic import BaseModel
from sqlalchemy import String
from sqlalchemy import create_engine, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import sessionmaker

#engine = create_engine('postgresql://tiims-subscription-management:pwd@172.26.165.187:5432/trading-db')
# Docker-Config
engine = create_engine('postgresql://nobodysforex:pwd@db:6432/trading-db')
Session = sessionmaker(bind=engine)
session = Session()

symbols = ["EURUSD", "GBPUSD", "XRPUSD", "XAGUSD"]

class TimeFrame(enum.Enum):
    PERIOD_M1 = 1
    PERIOD_M15 = 15
    PERIOD_H1 = 60
    PERIOD_H4 = 240
    PERIOD_D1 = 6*240
    PERIOD_W1 = 30*6*240

class Base(DeclarativeBase):
    pass


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

    def as_dict(self):
        #return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class TradeActivationDto(BaseModel):
    symbol:str
    timestamp:str
    magic:int
    open_price:float

class TradeUpdateDto(BaseModel):
    symbol:str
    timestamp:str
    magic:int
    profit: float
    swap:float
    closed:str
    commision:float

def storeTrade(trade: Trade):
    session.add(trade)
    session.commit()

def getUnActiveTrades():
    return session.query(Trade).filter(Trade.tradeid == 0, Trade.activated =="", Trade.openprice == 0.0).all()

def activeTrade(tradeActivationDto:TradeActivationDto):
    #print("Activating Trade", tradeActivationDto)

    #storeTrade = session.query(Trade).filter(Trade.symbol == tradeActivationDto.symbol, Trade.id == tradeActivationDto.magic).first()
    storeTrade = session.query(Trade).filter(Trade.symbol == tradeActivationDto.symbol, Trade.id == tradeActivationDto.magic).first()
    storeTrade.activated=tradeActivationDto.timestamp
    storeTrade.openprice=tradeActivationDto.open_price
    session.commit()
    #print("Trade Activated:", storeTrade.openprice)

def updateTrade(tradeUpdateDto:TradeUpdateDto):
    #print("Updating Trade", tradeUpdateDto)

    #storeTrade = session.query(Trade).filter(Trade.symbol == tradeActivationDto.symbol, Trade.id == tradeActivationDto.magic).first()
    storeTrade = session.query(Trade).filter(Trade.symbol == tradeUpdateDto.symbol, Trade.id == tradeUpdateDto.magic).first()
    if storeTrade is not None:
        storeTrade.swap = tradeUpdateDto.swap
        storeTrade.profit = tradeUpdateDto.profit
        storeTrade.commision = tradeUpdateDto.commision
        if tradeUpdateDto.closed is not None and tradeUpdateDto.closed != "" and tradeUpdateDto.closed != "-":
            storeTrade.closed = tradeUpdateDto.closed

        session.commit()
    #print("Trade Updated:", storeTrade)

def initTradingDb():
    Base.metadata.create_all(engine)