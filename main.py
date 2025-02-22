from momentum_calculator.scrape_sp500 import scrape_sp500_tickers
from momentum_calculator.calculator import calculate_momentum_and_smoothness

def main():
    scrape_sp500_tickers()
    calculate_momentum_and_smoothness('sp500_tickers.csv')

if __name__ == "__main__":
    main()