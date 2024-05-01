from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import numpy as np
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=20*365)
# Empty DataFrame to store fetched data
etf_data = pd.DataFrame()

# Import plotly
import plotly.graph_objects as go

etf_tickers = {
    "U.S. Stocks": "VTI",  # Vanguard Total Stock Market ETF
    "International Stocks": "VXUS",  # Vanguard Total International Stock ETF
    "U.S. Bonds": "BND",  # Vanguard Total Bond Market ETF
    "Real Estate": "VNQ",  # Vanguard Real Estate ETF
    "Commodities": "GSG",  # iShares S&P GSCI Commodity-Indexed Trust
    "Gold": "GLD",  # SPDR Gold Trust
    "Cash (3-Month U.S. Treasury Bills)": "BIL"  # SPDR Bloomberg Barclays 1-3 Month T-Bill ETF
}

def plotMonthlyReturns(etf_returns):
    annualized_returns = (1 + etf_returns).mean()**12 - 1
    # Format the annualized returns as percentages with two decimal places
    annualized_returns_pct = annualized_returns.apply(lambda x: '{:.2%}'.format(x))
    # Create a bar chart
    fig = go.Figure(data=[
        go.Bar(x=annualized_returns, y=annualized_returns.index, orientation='h',
               text=annualized_returns_pct, textposition='auto')
    ])
    # Customize plot layout
    fig.update_layout(
        title='Annualized Returns per Asset Class',
        xaxis_title='Annualized Return',
        yaxis_title='Asset Class',
        autosize=False,
        width=800,
        height=500,
        margin=dict(l=100),
        bargap=0.15
    )
    # Display the plot
    fig.show()

def plotPortfolioGrowth(etf_returns):
    # Calculate cumulative returns for a $100,000 investment in each asset class
    etf_cumulative_returns = (etf_returns + 1).cumprod() * 100000
    # Create a line chart with plotly to visualize the growth of $100,000 investment in each asset class
    import plotly.graph_objects as go
    line_chart = go.Figure()
    for asset_class in etf_cumulative_returns.columns:
        line_chart.add_trace(go.Scatter(x=etf_cumulative_returns.index, y=etf_cumulative_returns[asset_class], mode='lines', name=asset_class))
    line_chart.update_layout(
        title='Growth of $100,000 Investment Over Time',
        xaxis_title='Year',
        yaxis_title='Value of $100,000 Investment',
    )
    line_chart.show()

def plotHeatMap(etf_returns):
    # Calculate correlation matrix
    correlation_matrix = etf_returns.corr()
    # Create a heatmap
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    # Display the plot with a title
    plt.title('Correlations between Asset Classes over 20 Years')
    plt.show()

def plotRisk(etf_returns):
    # Calculate annual standard deviations
    annual_std_dev = etf_returns.std() * np.sqrt(12)
    # Format the annual std devs as percents with two decimal places
    annual_std_dev_pct = annual_std_dev.apply(lambda x: '{:.2%}'.format(x))
    # Create a bar chart
    fig_std = go.Figure(data=[
        go.Bar(x=annual_std_dev, y=annual_std_dev.index, orientation='h',
               text=annual_std_dev_pct, textposition='auto')
    ])
    # Customize plot layout
    fig_std.update_layout(
        title='Annual Standard Deviation per Asset Class',
        xaxis_title='Standard Deviation',
        yaxis_title='Asset Class',
        autosize=False,
        width=800,
        height=500,
        margin=dict(l=100),
        bargap=0.15
    )
    # Display the plot
    fig_std.show()

def plotSharpeRatio(etf_returns):
    annualized_returns = (1 + etf_returns).mean()**12 - 1
    # Calculate annual standard deviations
    annual_std_dev = etf_returns.std() * np.sqrt(12)
    # Format the annual std devs as percents with two decimal places
    annual_std_dev_pct = annual_std_dev.apply(lambda x: '{:.2%}'.format(x))
    # Set risk-free rate
    risk_free_rate = 0.02  # assuming a risk-free rate of 2%
    # Calculate excess returns for each asset class
    excess_returns = etf_returns - risk_free_rate / 12  # we divide by 12 to annualize the risk-free rate
    # Calculate Sharpe Ratio
    sharpe_ratio = excess_returns.mean() / excess_returns.std()
    sharpe_ratio = sharpe_ratio * np.sqrt(12)  # adjust for annualization
    # Create scatter plot
    plt.figure(figsize=(10, 7))
    plt.scatter(annualized_returns, annual_std_dev, c=sharpe_ratio,
                cmap='coolwarm', s=sharpe_ratio*400, alpha=0.6, edgecolors='w')  # sizing points by Sharpe Ratio
    plt.colorbar(label='Sharpe Ratio')
    plt.xlabel('Annualized Return')
    plt.ylabel('Annual Std Dev')
    plt.title('Asset Class Performance: Sharpe Ratio, Return & Risk')
    # Annotate asset class labels
    for i, txt in enumerate(etf_tickers.keys()):
        plt.annotate(txt, (annualized_returns[i], annual_std_dev[i]))
    plt.show()

if __name__ == "__main__":
    #print("Hello World")
    # Iterate, fetch data and update DataFrame
    for asset_class, ticker in etf_tickers.items():
        try:
            ticker_data = pdr.get_data_yahoo(ticker, start=start_date, end=end_date, interval = "1mo")
            # Keep only the Adjusted Close price, which accounts for splits and dividends
            ticker_data = ticker_data[['Adj Close']]
            ticker_data.columns = [asset_class]
            if etf_data.empty:
                etf_data = ticker_data
            else:
                etf_data = etf_data.join(ticker_data, how='outer')
        except Exception as e:
            print(f"There was an issue fetching the data for {ticker}: {str(e)}")
    #print(etf_data)

    # Calculate monthly returns
    etf_returns = etf_data.pct_change()
    # Handle missed data/NA values
    etf_returns.fillna(0, inplace=True)
    # Display the monthly returns
    print(etf_returns)

    plotMonthlyReturns(etf_returns)
    plotPortfolioGrowth(etf_returns)
    plotHeatMap(etf_returns)
    # does not load??
    #plotRisk(etf_returns)
    plotSharpeRatio(etf_returns)