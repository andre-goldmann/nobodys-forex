from sqlalchemy import create_engine
import pandas as pd
from backtesting import Backtest, Strategy
from trading_strategies.adx_crossover import AdxCrossover
from trading_strategies.aroon_adx import AroonAdx
from backtesting.lib import crossover
from bokeh.models import DatetimeTickFormatter
from backtesting.test import SMA

class SmaCross(Strategy):
    n1 = 10
    n2 = 20

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()

def main():
    # Database connection details
    db_host = "172.31.138.212:6432"
    db_name = "trading-db"
    db_user = "nobodysforex"
    db_password = "pwd"

    # Create SQLAlchemy engine
    engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}")

    # SQL query to fetch data
    query = """
    SELECT * FROM "Candles"
    WHERE "SYMBOL" = 'EURUSD' and "TIMEFRAME"='PERIOD_M15'
    ORDER BY "DATETIME" DESC
    LIMIT 5000
    """

    # Load data into pandas DataFrame
    df = pd.read_sql(query, engine)

    # Prepare data for backtesting
    df['Time'] = pd.to_datetime(df['DATETIME'])
    df = df.set_index('DATETIME')
    df = df.rename(columns={
        'OPEN': 'Open',
        'HIGH': 'High',
        'LOW': 'Low',
        'CLOSE': 'Close',
        'TICKVOL': 'Volume'
    })
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    print(df.tail())
    # Run backtest
    bt = Backtest(df, SmaCross, cash=10000, commission=.002)
    #bt = Backtest(df, AroonAdx, cash=10000, commission=.002)

    results = bt.run()

    # Print results
    print(results)

    # Plot the backtest results
    bt.plot(resample=False)

    # Save the plot
    bt.plot(filename='adx_crossover_backtest_results.html', open_browser=False)

    print("Backtest results saved to 'adx_crossover_backtest_results.html'")

if __name__ == "__main__":
    main()
