import json

import pandas as pd
from pydantic import BaseModel
from sqlalchemy import String, Enum, DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from DataBaseManagement import Base, TimeFrame, session, engine
from utils import loadData
#from kafka import  KafkaProducer

#docker inside
#producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
#producer = KafkaProducer(bootstrap_servers='172.30.218.157:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))


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

def storeCandleInDb(candle:CandlesDto):

    #producer.send('test:1:1', b'another_message')
    #producer.send('test:1:1',
    #              {"symbol": candle.symbol,
    #                    "TIMEFRAME": candle.TIMEFRAME,
    #                    "DATETIME": candle.DATETIME,
    #                    "OPEN": candle.OPEN,
    #                    "HIGH": candle.HIGH,
    #                    "LOW": candle.LOW,
    #                    "CLOSE": candle.CLOSE,
    #                    "TICKVOL": candle.TICKVOL,
    #                    "VOL": candle.VOL,
    #                    "SPREAD": candle.SPREAD})

    #producer.send('test:1:1',
    #              {'foo': 'bar'})


    #print("Entries: ", session.query(CandlesEntity.TIMEFRAME).count())
    timeFrame:TimeFrame = TimeFrame.__dict__[candle.TIMEFRAME]
    count = session.query(CandlesEntity).filter(CandlesEntity.SYMBOL == candle.symbol,
                                                CandlesEntity.TIMEFRAME == timeFrame,
                                                CandlesEntity.CLOSE == candle.CLOSE,
                                                CandlesEntity.OPEN == candle.OPEN).count()

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
        print(f"Stored: {candle}")
        session.add(spongebob)
        session.commit()
    else:
        print("Allreadys exists!!!")


def lastCandle(symbol:str, timeFrame:TimeFrame):
    last = session.query(CandlesEntity).filter(CandlesEntity.SYMBOL == symbol, CandlesEntity.TIMEFRAME == timeFrame).order_by(CandlesEntity.DATETIME.desc()).first()
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


#if __name__ == "__main__":
 #   initTradingDb()
    #TODO on startup go through like this load the last candle and from this candle on load all until now other metatrade

  #  lastCandle:CandlesDto = CandlesDto()
    # "EURUSD",TimeFrame.PERIOD_W1, "2023.10.08 00:00:00",1.0553, 1.06396, 1.05194, 1.06225,291058,0, 0

    timeframeEnum: TimeFrame = TimeFrame.__dict__[lastCandle.TIMEFRAME]

    #if timeframeEnum != TimeFrame.PERIOD_M1:
        #storeCandleInDb(lastCandle)

    #storeData("EURUSD",TimeFrame.PERIOD_W1)

    #for symbol in symbols:
    #    for timeFrame in TimeFrame:
    #        if TimeFrame.PERIOD_M1 is not timeFrame:
    #            storeData(symbol,timeFrame)
    #            loadDfFromDb(symbol, timeFrame)
  #  for symbol in symbols:
 #       for timeFrame in TimeFrame:
   #         if TimeFrame.PERIOD_M1 is not timeFrame:
    #            timeFrameStr = timeFrame.name.replace("PERIOD_", "")
     #           file = f"data/{symbol}_{timeFrameStr}.csv"
      #          df = loadData(file)
