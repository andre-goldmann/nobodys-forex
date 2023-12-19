import enum
import os
import sys
import traceback
from datetime import datetime
from datetime import timedelta
from enum import unique
from timeit import default_timer as timer

import pandas as pd
import statsmodels.api as sm
from dotenv import load_dotenv
from pydantic import BaseModel
from sqlalchemy import Enum, text
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy import create_engine, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import sessionmaker

from utils import loadData

load_dotenv()

# Docker-Config
engine = create_engine(os.environ['POSTGRES_URL'], pool_size=10, max_overflow=0)
Session = sessionmaker(bind=engine)

symbols = ["AUDUSD", "AUDCHF", "AUDJPY", "AUDNZD", "CHFJPY", "EURUSD", "EURCHF", "EURNZD", "GBPUSD", "GBPCAD", "GBPCHF", "GBPNZD",  "XAGUSD", "USDCAD", "USDCHF", "XRPUSD"]
tradeTypes = ["buy", "sell"]

@unique
class SupportResistanceType(enum.Enum):
    SUPPORT = 0
    RESISTANCE = 1

@unique
class TimeFrame(enum.Enum):
    PERIOD_M1 = 1
    PERIOD_M15 = 15
    PERIOD_H1 = 60
    PERIOD_H4 = 240
    PERIOD_D1 = 6*240
    PERIOD_W1 = 30*6*240

class Base(DeclarativeBase):
    pass

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

class SupportResistance(Base):
    __tablename__ = "SupportResistance"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(6))
    timeframe: Mapped[Enum] = mapped_column(Enum(TimeFrame))
    type: Mapped[Enum] = mapped_column(Enum(SupportResistanceType))
    level: Mapped[float]
    caclulator: Mapped[str]

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
    exit: Mapped[float] = mapped_column(nullable=True, default=0.0)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

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

class IgnoredSignal(Base):
    __tablename__ = "IgnoredSignals"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    json: Mapped[str] = mapped_column(String(64000))
    reason: Mapped[str] = mapped_column(String(64000))

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
    exit:float

class CandlesDto(BaseModel):
    #wird nicht gespeichert, für jedes Symbol ein DB
    symbol:str
    TIMEFRAME:str
    DATETIME:str
    OPEN:float
    HIGH:float
    LOW:float
    CLOSE:float
    TICKVOL:float
    VOL:float
    SPREAD:int

class SignalId(BaseModel):
    id: int

def storeData(symbol:str, timeFrame:TimeFrame):
    print(f"storeData for: {symbol}-{timeFrame}")

    timeFrameStr = timeFrame.name.replace("PERIOD_", "")
    file = f"data/{symbol}_{timeFrameStr}.csv"
    df = loadData(file)

    #import pandas_ta as ta
    #if TimeFrame.PERIOD_M15 == timeFrame:
    #   df["EMA20"] = ta.ema(df["CLOSE"], length=200)
    #  dfD1 = loadData('data/EURUSD_Daily_201501020000_202309290000.csv')

    df['TIMEFRAME'] = timeFrame.name
    if TimeFrame.PERIOD_D1 == timeFrame or TimeFrame.PERIOD_W1 == timeFrame:
        df['TIME'] = "00:00:00"
    df['SYMBOL'] = symbol
    df['DATETIME'] = df['DATE'] + ' ' + df['TIME']
    #df['TIMESTAMP'] =  df['DATETIME'].map(lambda dtStr: time.mktime(datetime.datetime.strptime(dtStr, "%Y.%m.%d %H:%M:%S").timetuple()))
    df['DATETIME'] = df['DATETIME'].astype('datetime64[s]')
    df = df.set_index('DATETIME')
    df.drop(columns=['DATE', 'TIME'])
    df = df.dropna()
    df = df.drop('DATE', axis=1)
    df = df.drop('TIME', axis=1)
    df.to_sql(name='Candles', con=engine, if_exists='append')

def storeSignal(signal: Signal):
    with Session.begin() as session:
        session.add(signal)
        session.commit()
        session.close()

def modifySignalInDb(id:int, type:str, entry:float, sl:float, tp:float, lots:float):
    with Session.begin() as session:
        storeSignal = session.query(Signal).filter(Signal.id == id).first()
        if storeSignal is not None:
            storeSignal.type=type
            storeSignal.entry=entry
            storeSignal.sl=sl
            storeSignal.tp=tp
            storeSignal.lots=lots
            session.commit()
            session.close()

def storeCandleInDb(candle:CandlesDto):
    with Session.begin() as session:

        timeFrame:TimeFrame = TimeFrame.__dict__[candle.TIMEFRAME]
        candleTime = datetime.strptime(candle.DATETIME, "%Y.%m.%d %H:%M")
        count = session.query(CandlesEntity).filter(CandlesEntity.SYMBOL == candle.symbol,
                                                    CandlesEntity.TIMEFRAME == timeFrame,
                                                    CandlesEntity.DATETIME == candleTime).count()
        #print(f"Found {count} for {candle}")
        if count == 0:
            spongebob = CandlesEntity(
                SYMBOL=candle.symbol,
                TIMEFRAME= timeFrame,
                DATETIME=candleTime,
                OPEN=candle.HIGH,
                HIGH=candle.HIGH,
                LOW=candle.LOW,
                CLOSE=candle.CLOSE,
                TICKVOL=candle.TICKVOL,
                VOL=candle.VOL,
                SPREAD=candle.SPREAD,
            )
            last = lastCandle(candle.symbol, timeFrame)
            print(f"New: {candle} ----- last {last}")
            session.add(spongebob)
            session.commit()
            session.close()
        else:
            print("Allreadys exists:" + str(candle))


def lastCandle(symbol:str, timeFrame:TimeFrame):
    with Session.begin() as session:
        candle = session.query(CandlesEntity).filter(CandlesEntity.SYMBOL == symbol, CandlesEntity.TIMEFRAME == timeFrame).order_by(CandlesEntity.DATETIME.desc()).first()
        session.expunge(candle)
        session.close()
        return candle

def loadDfFromDb(symbol:str, timeFrame:TimeFrame, limit=250000):
    with Session.begin() as session:
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
            .limit(limit)
            .statement,
            con = engine
        )
        print(len(df), " database entries loaded for ",timeFrame)
        print("Last row: ")
        print(df.iloc[-1])
        #There are a lot of duplicates stored, thats why we need to remove them
        df_no_duplicates = df.drop_duplicates(subset=['DATETIME'])
        return df_no_duplicates.drop_duplicates()

def countEntries(symbol:str, timeFrame:TimeFrame):
    with Session.begin() as session:
        count = session.query(CandlesEntity).filter(CandlesEntity.SYMBOL == symbol, CandlesEntity.TIMEFRAME == timeFrame).count()
        session.close()
        return count

def countTrades():
    with Session.begin() as session:
        count = session.query(Signal).count()
        session.close()
        return count

def deleteSignalInDb(id:int):
    with Session.begin() as session:
        storeSignal = session.query(Signal).filter(Signal.id == id).first()
        if storeSignal is not None:
            session.delete(storeSignal)
            session.commit()
            session.close()

def getIgnoredSignals():
    with Session.begin() as session:
        signals = session.query(IgnoredSignal).all()
        session.expunge_all()
        session.close()
        return signals

def getWaitingSignals():
    with Session.begin() as session:
        signals = session.query(Signal.id,
                             Signal.symbol,
                             Signal.type,
                             Signal.entry,
                             Signal.sl,
                             Signal.tp,
                             Signal.lots,
                             Signal.stamp,
                             Signal.strategy).filter(Signal.tradeid == 0, Signal.activated == "", Signal.openprice == 0.0).all()
        session.expunge_all()
        session.close()
        return signals

def getWaitingSignalsProd():
    with Session.begin() as session:
        signals = session.query(ProdSignal.id,
                                ProdSignal.symbol,
                                ProdSignal.type,
                                ProdSignal.entry,
                                ProdSignal.sl,
                                ProdSignal.tp,
                                ProdSignal.lots,
                                ProdSignal.stamp,
                                ProdSignal.strategy).filter(ProdSignal.tradeid == 0, ProdSignal.activated == "", ProdSignal.openprice == 0.0).all()
        session.expunge_all()
        session.close()
        return signals

def deleteSignalFromDb(id:SignalId):
    with Session.begin() as session:
        session.query(Signal).filter(Signal.id == id.id).delete()
        session.commit()
        session.close()

def deleteIgnoredSignalFromDb(id:SignalId):
    with Session.begin() as session:
        session.query(Signal).filter(IgnoredSignal.id == id.id).delete()
        session.commit()
        session.close()

def getExecutedSignals(strategy:str):
    with Session.begin() as session:
        signals = session.query(Signal.id,
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
                             Signal.closed,
                             Signal.exit).filter(Signal.strategy == strategy, Signal.openprice > 0.0).order_by(Signal.stamp.desc()).all()
        session.expunge_all()
        session.close()
        return signals

def getStrategystats():
    with Session.begin() as session:
        signalStats = session.query(Signal.strategy,
                             func.count(Signal.id).filter(Signal.profit != 0).label("alltrades"),
                             func.count(Signal.id).filter(Signal.profit < 0).label("failedtrades"),
                             func.count(Signal.id).filter(Signal.profit > 0).label("successtrades"),
                             func.sum(Signal.profit).label("profit"),
                             func.sum(Signal.commision).label("commission"),
                             func.sum(Signal.swap).label("swap")).group_by(Signal.strategy).all()
        session.expunge_all()
        session.close()
        return signalStats

def getInstrumentstats(strategy:str):

    with Session.begin() as session:
        signalStats = session.query(Signal.symbol,
                                    func.count(Signal.id).filter(Signal.profit != 0).label("alltrades"),
                                    func.count(Signal.id).filter(Signal.profit < 0).label("failedtrades"),
                                    func.count(Signal.id).filter(Signal.profit > 0).label("successtrades"),
                                    func.sum(Signal.profit).label("profit"),
                                    func.sum(Signal.commision).label("commission"),
                                    func.sum(Signal.swap).label("swap")).filter(Signal.strategy == strategy).group_by(Signal.symbol).all()
        session.expunge_all()
        session.close()
        return signalStats

def activateSignal(tradeActivationDto:SignalActivationDto):
    #print("Activating Trade", tradeActivationDto)
    with Session.begin() as session:
        storeSignal = session.query(Signal).filter(Signal.symbol == tradeActivationDto.symbol, Signal.id == tradeActivationDto.magic).first()
        storeSignal.activated=tradeActivationDto.timestamp
        storeSignal.openprice=tradeActivationDto.open_price
        session.commit()
        session.close()

def activateSignalProd(tradeActivationDto:SignalActivationDto):
    #print("Activating Trade", tradeActivationDto)
    with Session.begin() as session:
        storeSignal = session.query(ProdSignal).filter(ProdSignal.symbol == tradeActivationDto.symbol, ProdSignal.id == tradeActivationDto.magic).first()
        storeSignal.activated=tradeActivationDto.timestamp
        storeSignal.openprice=tradeActivationDto.open_price
        session.commit()
        session.close()
    #print("Trade Activated:", storeSignal.openprice)

def updateSignalInDb(signalUpdateDto:SignalUpdateDto):
    #print("Updating Trade", tradeUpdateDto)

    with Session.begin() as session:
        storedSignal = session.query(Signal).filter(Signal.symbol == signalUpdateDto.symbol, Signal.id == signalUpdateDto.magic).first()
        if storedSignal is not None:
            storedSignal.swap = signalUpdateDto.swap
            storedSignal.profit = signalUpdateDto.profit
            storedSignal.commision = signalUpdateDto.commision
            if signalUpdateDto.closed is not None and signalUpdateDto.closed != "" and signalUpdateDto.closed != "-":
                storedSignal.closed = signalUpdateDto.closed

            session.commit()
            session.close()

def updateSignalProdInDb(signalUpdateDto:SignalUpdateDto):
    #print("Updating Trade", tradeUpdateDto)

    with Session.begin() as session:
        storedSignal = session.query(ProdSignal).filter(ProdSignal.symbol == signalUpdateDto.symbol, ProdSignal.id == signalUpdateDto.magic).first()
        if storedSignal is not None:
            storedSignal.swap = signalUpdateDto.swap
            storedSignal.profit = signalUpdateDto.profit
            storedSignal.commision = signalUpdateDto.commision
            if signalUpdateDto.closed is not None and signalUpdateDto.closed != "" and signalUpdateDto.closed != "-":
                storedSignal.closed = signalUpdateDto.closed

            session.commit()
            session.close()

def getLinesInfo(symbol, timeframeEnum):
    with Session.begin() as session:
        infos = session.query(Regressions).filter(
            Regressions.symbol == symbol,
            Regressions.timeFrame == timeframeEnum).all()
        session.expunge_all()
        session.close()
        return infos

def updateSignalByHistory(historyUpdateDto:HistoryUpdateDto):
    #print("Updating Trade", tradeUpdateDto)
    print(historyUpdateDto)
    with Session.begin() as session:
        storedSignal = session.query(Signal).filter(Signal.symbol == historyUpdateDto.symbol, Signal.id == historyUpdateDto.magic).first()
        if storedSignal is not None:
            storedSignal.swap = historyUpdateDto.swap
            storedSignal.profit = historyUpdateDto.profit
            storedSignal.commision = historyUpdateDto.commision
            storedSignal.exit = historyUpdateDto.exit
            if historyUpdateDto.closed is not None and historyUpdateDto.closed != "" and historyUpdateDto.closed != "-":
                storedSignal.closed = historyUpdateDto.closed

            session.commit()
            session.close()
            print("Updated Signal")
        else:
            print("No Signal found for: " + str(historyUpdateDto))

def regressionCalculation(symbol:str, startDate:str, timeFrame:TimeFrame):

    start = timer()

    df = loadDfFromDb(symbol, timeFrame)
    #print("Len before: ", len(df))
    mask = (df['DATETIME'] >= startDate)
    df = df.loc[mask]
    #print("Len after: ", len(df))

    #print("First row: ", df.iloc[0]['DATETIME'])
    lsma_arr = []
    dates_arr = []

    for i in range(len(df) - 24):
        input_reg = df[i:25+i]
        x = pd.Series(range(len(input_reg.index))).values
        y = input_reg.HIGH
        model = sm.OLS(y, sm.add_constant(x)).fit()
        pred = model.predict()[-1]
        lsma_arr.append(pred)
        dates_arr.append(input_reg.iloc[-1].name)

    lsma_df = pd.DataFrame({'LSMA': lsma_arr}, index=dates_arr)

    all_df = pd.concat([lsma_df,df], axis=1)
    all_df.dropna(inplace=True)

    print("StartTime: ", all_df.iloc[0]['DATETIME'])
    print("endTime:  ", all_df.iloc[-1]['DATETIME'])
    print("###################################")

    end = timer()
    print("Regression took: ", timedelta(seconds=end-start))

    deleteRegressionData(symbol, timeFrame)

    with Session.begin() as session:

        spongebob = Regressions(
            symbol=symbol,
            timeFrame= timeFrame.name,
            startTime= all_df.iloc[0].DATETIME,
            endTime=all_df.iloc[-1].DATETIME,
            startValue=all_df.iloc[0].LSMA,
            endValue=all_df.iloc[-1].LSMA,
        )

        session.add_all([spongebob])
        session.commit()
        session.close()

def deleteRegressionData(symbol:str, timeFrame:TimeFrame):
    with Session.begin() as session:
        try:
            results = session.query(Regressions).filter(Regressions.symbol==symbol, Regressions.timeFrame==timeFrame).all()

            for r in results:
                session.delete(r)
            session.commit()
            session.close()
        except Exception:
            print("Exception while deleting Regressions:")
            print("-"*60)
            traceback.print_exc(file=sys.stdout)
            print("-"*60)
            session.rollback()
            session.close()

def getSrLevels(symbol:str):
    with Session.begin() as session:
        levels = session.query(SupportResistance).filter(
            SupportResistance.symbol == symbol
        ).all()
        session.expunge_all()
        session.close()
        return levels

def deleteSupportResistance(symbol:str, timeFrame:TimeFrame):
    with Session.begin() as session:
        try:
            results = session.query(SupportResistance).filter(
                SupportResistance.symbol==symbol,
                SupportResistance.timeframe==timeFrame).all()
            for r in results:
                session.delete(r)
            session.commit()
            session.close()
        except Exception:
            print("Exception while deleting SupportResistance:")
            print("-"*60)
            traceback.print_exc(file=sys.stdout)
            print("-"*60)
            session.rollback()
            session.close()

def storeSupportResistance(sr:SupportResistance):
    # nur jeden Tage einmal löschen
    #deleteSupportResistance(sr.symbol)

    with Session.begin() as session:
        session.add(sr)
        session.commit()
        session.close()

def loadSrs(symbol:str):
    with Session.begin() as session:
        count = session.query(SupportResistance).filter(SupportResistance.symbol==symbol).all()
        session.close()
        return count

def insertFromFile(file:str):
    print("Inserting trades...")
    with open(file, 'r') as file:
        data_df = pd.read_csv(file)
        df2 = data_df.iloc[: , 1:]
        for index, row in df2.iterrows():

            storeSignal(Signal(
                symbol=row['symbol'],
                type=row['type'],
                entry=row['entry'],
                sl=row['sl'],
                tp=row['tp'],
                lots=row['lots'],
                spread=row['spread'],
                tradeid=row['tradeid'],
                stamp=row['stamp'],
                activated=row['activated'],
                openprice=row['openprice'],
                swap=row['swap'],
                profit=row['profit'],
                closed=row['closed'],
                commision=row['commision'],
                strategy=row['strategy']
            ))

        print("Trades stored")

def add_column(table_name):
    #column_name = column.compile(dialect=engine.dialect)
    #column_type = column.type.compile(engine.dialect)
    connection = engine.connect()
    statement = text(f'ALTER TABLE {table_name} ADD exit float;')
    #connection.execute('ALTER TABLE %s ADD COLUMN %s %s' % (table_name, column_name, column_type))
    connection.execute(statement)


def initTradingDb():
    #column = Column('exit', Float, primary_key=False, default=0.0, nullable=True)
    #add_column("public.Trades")
    #Trade.__table__.drop(engine)
    Base.metadata.create_all(engine)

def dropAllTables():
    Base.metadata.drop_all(engine)   # all tables are deleted

def countSignals(strategy, symbol):
    with Session.begin() as session:
        count = session.query(Signal).filter(Signal.activated == "", Signal.openprice == 0.0, Signal.symbol == symbol, Signal.strategy == strategy).count()
        session.close()
        return count