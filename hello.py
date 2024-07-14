from sqlalchemy import create_engine
import pandas as pd
from backtesting import Backtest
from trading_strategies.adx_crossover import AdxCrossover

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
    """

    # Load data into pandas DataFrame
    df = pd.read_sql(query, engine)

    # Prepare data for backtesting
    df['Time'] = pd.to_datetime(df['TIME'])
    df = df.set_index('Time')
    df = df.rename(columns={
        'OPEN': 'Open',
        'HIGH': 'High',
        'LOW': 'Low',
        'CLOSE': 'Close',
        'TICKVOL': 'Volume'
    })
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]

    # Run backtest
    bt = Backtest(df, AdxCrossover, cash=10000, commission=.002)
    results = bt.run()

    # Print results
    print(results)

    # Plot the backtest results
    bt.plot()

    # Save the plot
    bt.plot(filename='adx_crossover_backtest_results.html', open_browser=False)

    print("Backtest results saved to 'adx_crossover_backtest_results.html'")

if __name__ == "__main__":
    main()
