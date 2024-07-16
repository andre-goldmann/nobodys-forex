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
        self.df = self.data
        self.df['20ema'] = self.df['Close'].ewm(span=20, adjust=False).mean()
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
    WHERE "SYMBOL" = 'EURUSD' and "TIMEFRAME"='PERIOD_H1'
    ORDER BY "DATETIME" DESC
    LIMIT 1000
    """

    # Load data into pandas DataFrame
    df = pd.read_sql(query, engine)

    # Prepare data for backtesting
    #df['Time'] = pd.to_datetime(df['DATETIME'])
    df = df.set_index('DATETIME')
    df = df.rename(columns={
        'OPEN': 'Open',
        'HIGH': 'High',
        'LOW': 'Low',
        'CLOSE': 'Close',
        'TICKVOL': 'Volume'
    })
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    #print(df.tail())
    # Run backtest
    # works
    bt = Backtest(df, SmaCross, cash=10000, commission=.002)
    #bt = Backtest(df, AdxCrossover, cash=10000, commission=.002)
    #bt = Backtest(df, AroonAdx, cash=10000, commission=.002)

    #results = bt.run()
    stats = bt.run()
    stats
    stats = bt.optimize(n1=range(5, 30, 5),
                        n2=range(10, 70, 5),
                        maximize='Equity Final [$]',
                        constraint=lambda param: param.n1 < param.n2)
    print(stats)

    # Print results
    #print(results)

    # Plot the backtest results
    #bt.plot(resample=False,
    #        plot_width=1200,
    #        plot_height=800,
    #        xaxis_kwargs={'formatter': DatetimeTickFormatter(days='%d %b')})

    # Save the plot
    #bt.plot(filename='adx_crossover_backtest_results.html', open_browser=False)
    #bt.run()
    #bt.plot()

    print("Backtest results saved to 'adx_crossover_backtest_results.html'")

if __name__ == "__main__":
    main()
