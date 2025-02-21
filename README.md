# Stock Momentum Calculator

This repository contains a Python script that downloads historical stock data for S&P 500 companies and calculates both momentum and smoothness metrics for each stock over a specified time period.

## Overview

The script uses [yfinance](https://pypi.org/project/yfinance/) to retrieve daily historical stock prices for the tickers listed in the CSV file `sp500_tickers.csv` (located in the `data` folder). The data is then transformed into a long-format DataFrame and processed to:

- Calculate weekly closing prices by grouping daily data by week.
- Compute **momentum** for each stock based on the ratio between the current week's closing price and the closing price from four weeks ago.
- Compute **smoothness** as a measure of how consistently the stock's price has increased week over week.

The final results are saved in an Excel file (`momentum_smooth_by_ticker.xlsx`) in the `output` folder.

## Features

- **Data Retrieval:** Downloads daily stock prices for specified tickers using Yahoo Finance.
- **Data Transformation:** Reshapes data from wide to long format with columns for `Date`, `Symbol`, and `Close`.
- **Weekly Aggregation:** Determines the week's start date (Monday) for each record and calculates the corresponding weekday number.
- **Momentum Calculation:** 
  - Computes the price from four weeks ago for each week.
  - Calculates weekly momentum as: 

  $\text{Momentum} = 1 + \frac{\text{Current Close} - \text{Close Four Weeks Ago}}{\text{Close Four Weeks Ago}}$
  
  - Aggregates the weekly momentum to obtain an overall momentum per stock.
- **Smoothness Calculation:** Measures the consistency of price increases from one week to the next.
- **Sorting and Output:** Sorts the results by momentum and smoothness, and exports the final DataFrame to an Excel file.

## Requirements

To install the necessary packages, use the `requirements.txt` file provided:

```bash
pip install -r requirements.txt
```

## Usage

To run the project from the terminal, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/JacobYoungT/Stock-Momentum-Calculator.git
cd Stock-Momentum-Calculator
```

2. Create and activate a virtual environment:

On Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

On macOS/Linux:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Run the main script:
```bash
python main.py
```

The script will:
1. First scrape the latest S&P 500 tickers (using `scrape_sp500.py`)
2. Download the historical data for each ticker
3. Calculate momentum and smoothness metrics
4. Save the results to `output/momentum_smooth_by_ticker.xlsx`

To deactivate the virtual environment when you're done:
```bash
deactivate
```
