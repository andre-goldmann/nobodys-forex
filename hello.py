from sqlalchemy import create_engine
import pandas as pd

def main():
    # Database connection details
    db_host = "172.31.138.212:6432"
    db_name = "trading-db"
    db_user = "nobodysforex"  # Replace with actual username
    db_password = "pwd"  # Replace with actual password

    # Create SQLAlchemy engine
    engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}")

    # SQL query to fetch data
    query = """
    SELECT * FROM "Candles"
    WHERE "SYMBOL" = 'EURUSD' and "TIMEFRAME"='PERIOD_M15'
    """

    # Load data into pandas DataFrame
    df = pd.read_sql(query, engine)

    # Print the first few rows of the DataFrame
    print(df.head())

    # Print the shape of the DataFrame
    print(f"DataFrame shape: {df.shape}")

if __name__ == "__main__":
    main()
