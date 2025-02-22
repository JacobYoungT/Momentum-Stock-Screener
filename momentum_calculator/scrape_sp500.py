import pandas as pd
import os
from momentum_calculator.config import data_dir

def scrape_sp500_tickers(
        link='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks',
        output_file='sp500_tickers.csv',
        _dir=data_dir
):
    os.makedirs(_dir, exist_ok=True)

    df = pd.read_html(link, header=0)[0]
    df = df['Symbol']

    # Write to .csv
    df.to_csv(os.path.join(_dir, output_file), index=False)
    print(f"Tickers saved to {output_file}")