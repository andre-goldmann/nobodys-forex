import pandas as pd
from pydantic import BaseModel
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from DataBaseManagement import Base, TimeFrame, session, engine, initTradingDb, symbols
from utils import loadData


class CandlesEntity(Base):
    __tablename__ = "Candles"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    SYMBOL: Mapped[str] = mapped_column(String(6))
    TIMEFRAME: Mapped[Enum] = mapped_column(Enum(TimeFrame))
    DATETIME: Mapped[str] = mapped_column(String(30))
    OPEN: Mapped[float]
    HIGH: Mapped[float]
    LOW: Mapped[float]
    CLOSE: Mapped[float]
    TICKVOL: Mapped[float]
    VOL: Mapped[float]
    SPREAD: Mapped[float]
    #STAMP: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())

    def __repr__(self) -> str:
        return (f"Candles(id={self.id!r}, DATETIME={self.DATETIME!r}"
                f", OPEN={self.OPEN!r}, CLOSE={self.CLOSE!r})")

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


def countEntries(symbol:str, timeFrame:TimeFrame):
    return session.query(CandlesEntity).filter(CandlesEntity.SYMBOL == symbol, CandlesEntity.TIMEFRAME == timeFrame).count()

def storeData(symbol:str, timeFrame:TimeFrame):
    print(f"storeData for: {symbol}-{timeFrame}")
    pairTimeFrameMap = {"EURUSD:PERIOD_M15": 'data/EURUSD_M15.csv',
                       "EURUSD:PERIOD_H1": 'data/EURUSD_H1.csv',
                       "EURUSD:PERIOD_H4": 'data/EURUSD_H4.csv',
                       "EURUSD:PERIOD_D1": 'data/EURUSD_Daily.csv',
                       "EURUSD:PERIOD_W1": 'data/EURUSD_Weekly.csv',

                        "XRPUSD:PERIOD_M15": 'data/XRPUSD_M15.csv',
                        "XRPUSD:PERIOD_H1": 'data/XRPUSD_H1.csv',
                        "XRPUSD:PERIOD_H4": 'data/XRPUSD_H4.csv',
                        "XRPUSD:PERIOD_D1": 'data/XRPUSD_Daily.csv',
                        "XRPUSD:PERIOD_W1": 'data/XRPUSD_Weekly.csv',

                        "GBPUSD:PERIOD_M15": "data/GBPUSD_M15.csv",
                        "GBPUSD:PERIOD_H1": "data/GBPUSD_H1.csv",
                        "GBPUSD:PERIOD_H4": "data/GBPUSD_H4.csv",
                        "GBPUSD:PERIOD_D1": "data/GBPUSD_Daily.csv",
                        "GBPUSD:PERIOD_W1": "data/GBPUSD_Weekly.csv",

                        "XAGUSD:PERIOD_M15": "data/XAGUSD_M15.csv",
                        "XAGUSD:PERIOD_H1": "data/XAGUSD_H1.csv",
                        "XAGUSD:PERIOD_H4": "data/XAGUSD_H4.csv",
                        "XAGUSD:PERIOD_D1": "data/XAGUSD_Daily.csv",
                        "XAGUSD:PERIOD_W1": "data/XAGUSD_Weekly.csv"
                        }

    file = pairTimeFrameMap[symbol + ":" + timeFrame.name]
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
    df['DATETIME'] = df['DATETIME'].astype('datetime64[s]')
    df = df.set_index('DATETIME')
    df.drop(columns=['DATE', 'TIME'])
    df = df.dropna()
    df = df.drop('DATE', axis=1)
    df = df.drop('TIME', axis=1)
    df.to_sql(name='Candles', con=engine, if_exists='append')

def storeCandleInDb(candle:CandlesDto):

    #print("Entries: ", session.query(CandlesEntity.TIMEFRAME).count())
    timeFrame:TimeFrame = TimeFrame.__dict__[candle.TIMEFRAME]
    print(candle)
    count = session.query(CandlesEntity).filter(CandlesEntity.SYMBOL == candle.symbol,
                                                CandlesEntity.TIMEFRAME == timeFrame,
                                                CandlesEntity.DATETIME == candle.DATETIME,
                                                CandlesEntity.CLOSE == candle.CLOSE).count()

    if count == 0:
        spongebob = CandlesEntity(
            SYMBOL=candle.symbol,
            TIMEFRAME= TimeFrame.__dict__[candle.TIMEFRAME].name,
            DATETIME= candle.DATETIME,
            OPEN=candle.HIGH,
            HIGH=candle.HIGH,
            LOW=candle.LOW,
            CLOSE=candle.CLOSE,
            TICKVOL=candle.TICKVOL,
            VOL=candle.VOL,
            SPREAD=candle.SPREAD,
        )
        session.add(spongebob)
        session.commit()
    else:
        print("Allreadys exists!!!")


def lastCandle(symbol:str, timeFrame:TimeFrame):
    last = session.query(CandlesEntity).filter(CandlesEntity.SYMBOL == symbol, CandlesEntity.TIMEFRAME == timeFrame).order_by(CandlesEntity.id.desc()).first()
    return last

#def lastCandle(symbol:str, timeFrame:TimeFrame):
#    return session.query(CandlesEntity.SYMBOL,
#                         CandlesEntity.TIMEFRAME,
#                         CandlesEntity.DATETIME,
#                         CandlesEntity.OPEN,
#                         CandlesEntity.HIGH,
#                         CandlesEntity.LOW,
#                         CandlesEntity.CLOSE,
#                         CandlesEntity.TICKVOL,
#                         CandlesEntity.VOL,
#                         CandlesEntity.SPREAD).filter(CandlesEntity.SYMBOL == symbol, CandlesEntity.TIMEFRAME == timeFrame).first()


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
    print("Last row: ")
    print(df.iloc[-1])
    return df


if __name__ == "__main__":
    initTradingDb()
    #TODO on startup go through like this load the last candle and from this candle on load all until now other metatrade
    for symbol in symbols:
        for timeFrame in TimeFrame:
            if TimeFrame.PERIOD_M1 is not timeFrame:
                storeData(symbol,timeFrame)
                loadDfFromDb(symbol, timeFrame)