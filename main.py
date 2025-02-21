import yfinance as yf
import pandas as pd
from datetime import timedelta, date
import os
from tqdm import tqdm
import warnings

'''
There is kind of a performance issue as we are appending are new row for each loop in the for loop...
Which is why we ignore the warning right now.
'''
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

# Set directories
current_dir = os.getcwd()
data_dir = os.path.join(current_dir, 'data')
output_dir = os.path.join(current_dir, 'output')

# Read tickers from data dir
tickers = pd.read_csv(os.path.join(data_dir, 'sp500_tickers.csv'))

# Define the time period and download data
## Define time period
start_date = date.today() - timedelta(weeks=52)
end_date = date.today() - timedelta(weeks=4)

print("Start:", start_date)
print("End:", end_date)

## Download stock data
stock_data = pd.DataFrame()
for ticker in tqdm(tickers['Symbol'], desc="Downloading stock data"):
    try:
        raw_data = yf.download(ticker, start=start_date, end=end_date, interval='1d', progress=False)
        raw_data['Symbol'] = ticker
        stock_data[ticker] = raw_data['Close']
    except Exception as e:
        print(f"Error downloading {ticker}: {e}")

stock_data.reset_index(inplace=True)
stock_data = pd.melt(stock_data, id_vars=['Date'], value_vars=tickers['Symbol'], var_name='Symbol', value_name='Close')

# Calculate weekly close prices
## Calculate week start date and weekday number
stock_data['WeekStartDate'] = stock_data['Date'] - pd.to_timedelta(stock_data['Date'].dt.dayofweek, unit='D')
stock_data['WeekDayNumber'] = stock_data['Date'].dt.weekday

## Group by 'Date' and 'WeekStartDate', and select the maximum 'WeekDayNumber' within each group
grouped_df = stock_data.groupby(['Symbol', 'WeekStartDate'])['WeekDayNumber'].max().reset_index()

## Merge to get the close price for max weekday number
friday_close_data = pd.merge(
    stock_data, grouped_df,
    on=['Symbol', 'WeekStartDate', 'WeekDayNumber'],
    how='inner'
)

# Calculate momentum
## Calculate the stock price four weeks ago for each date
friday_close_data['FourWeeksAgo'] = friday_close_data['WeekStartDate'] - pd.DateOffset(weeks=4)

## Perform af join operation to get the stock price four weeks ago
momentum_data = friday_close_data.merge(friday_close_data[['WeekStartDate', 'Symbol', 'Close']],
                                        left_on=['Symbol', 'FourWeeksAgo'], right_on=['Symbol', 'WeekStartDate'],
                                        suffixes=('', '_FourWeeksAgo'), how='left')

## Calculate the momentum for every week
momentum_data['Momentum'] = 1 + ((momentum_data['Close'] - momentum_data['Close_FourWeeksAgo']) /
                                 momentum_data['Close_FourWeeksAgo'])
mom_by_ticker = momentum_data.groupby(['Symbol'])['Momentum'].agg('prod') - 1
mom_by_ticker = mom_by_ticker.reset_index()

# Calculate smoothness
## Calculate the stock price one week ago for each date
friday_close_data['OneWeekAgo'] = friday_close_data['WeekStartDate'] - pd.DateOffset(weeks=1)

## Perform a join operation to get the stock price one week ago
momentum_data = friday_close_data.merge(friday_close_data[['WeekStartDate', 'Symbol', 'Close']],
                                        left_on=['Symbol', 'OneWeekAgo'], right_on=['Symbol', 'WeekStartDate'],
                                        suffixes=('', '_OneWeekAgo'), how='left')

## Calculate the smoothness for every week
momentum_data['Smoothness'] = momentum_data['Close'] - momentum_data['Close_OneWeekAgo']

## Get smoothness by ticker
smo_by_ticker = momentum_data.groupby('Symbol').agg(
    Smoothness=('Smoothness', lambda x: (x > 0).sum() / (len(x) - 1))
).reset_index()

# Combine momentum and smoothness
momentum_smooth_by_ticker = mom_by_ticker.merge(smo_by_ticker, on='Symbol', how='inner')

# Output to excel
momentum_smooth_by_ticker.to_excel(os.path.join(output_dir, 'momentum_smooth_by_ticker.xlsx'), index=False)