import sys
import traceback
from datetime import timedelta
from timeit import default_timer as timer

import pandas as pd
import statsmodels.api as sm
from sqlalchemy import Enum
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from CandleStorageHandler import loadDfFromDb
from DataBaseManagement import Base, Session, TimeFrame, engine


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


# TODO change file to symbol, add starting day
def regressionCalculation(symbol:str, startDate:str, timeFrame:TimeFrame):

    start = timer()

    df = loadDfFromDb(symbol, timeFrame)
    #print("Len before: ", len(df))
    mask = (df['DATETIME'] >= startDate)
    df = df.loc[mask]
    #print("Len after: ", len(df))

    print("First row: ", df.iloc[0]['DATETIME'])
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

    print("First row: ", all_df.iloc[0]['DATETIME'])
    print("Last row:  ", all_df.iloc[-1]['DATETIME'])
    print("###################################")

    end = timer()
    print("Regression took: ", timedelta(seconds=end-start))

    deleteRegressionData(symbol, timeFrame)

    with Session.begin() as session:

        spongebob = Regressions(
            symbol=symbol,
            timeFrame= timeFrame.name,
            #startTime= all_df.iloc[-lookback].DATETIME,
            startTime= all_df.iloc[0].DATETIME,
            endTime=all_df.iloc[-1].DATETIME,
            #startValue=all_df.iloc[-lookback].LSMA,
            startValue=all_df.iloc[0].LSMA,
            endValue=all_df.iloc[-1].LSMA,
        )

        session.add_all([spongebob])
        session.commit()

        dfFromDb = pd.read_sql_query(
            sql = session.query(Regressions.timeFrame,
                                Regressions.startTime,
                                Regressions.endTime,
                                Regressions.startValue,
                                Regressions.endValue).statement,
            con = engine
        )
        print(len(dfFromDb), " regression entries stored.")
        #print("Last row: ")
        #print(df.iloc[-1])

def deleteRegressionData(symbol:str, timeFrame:TimeFrame):
    with Session.begin() as session:
        try:
            results = session.query(Regressions).filter(Regressions.symbol==symbol, Regressions.timeFrame==timeFrame).all()
            #print(results)
            print("ToDelete:")
            for r in results:
                print(r)
                session.delete(r)
            session.commit()
        except Exception:
            print("Exception while deleting Regressions:")
            print("-"*60)
            traceback.print_exc(file=sys.stdout)
            print("-"*60)
            session.rollback()

