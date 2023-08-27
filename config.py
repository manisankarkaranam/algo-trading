import os


class Config:
    # Paths
    BASE_DIR = os.getcwd()

    RESOURCE_DIR = os.path.join(BASE_DIR, 'Resources')
    STOCK_SYMBOLS_CSV = os.path.join(RESOURCE_DIR, '{file_name}')
    STOCKS_HIS_DATA_DIR = os.path.join(RESOURCE_DIR, 'Stocks-Data')
    STOCKS_DOWNLOAD_DIR = os.path.join(STOCKS_HIS_DATA_DIR, '{date}')

    RESULTS_DIR = os.path.join(BASE_DIR, 'Results')
    RESULT_CSV = os.path.join(RESULTS_DIR, '{file_name}')

    # Urls
    HIS_DATA_FETCH_URL = "https://query1.finance.yahoo.com/v7/finance/download/" \
                         "{stock}.NS?period1=946684800&period2={epoch}&interval=1{candle_length}&" \
                         "events=history&includeAdjustedClose=true"

    # Settings
    IS_PLOT_NEEDED = False

    # Algorithms
    STOCKS_ALGO_CROSS_MA_FROM_BELOW_CSV = 'stocks-cross-ma-from-below.csv'
    TRADES_CROSS_MA_FROM_BELOW = 'result-cross-ma-from-below.csv'

    STOCKS_ALGO_BELOW_MA_RSI = 'stocks-below-ma-rsi.csv'
    TRADES_BELOW_MA_RSI = 'result-below-ma-rsi.csv'
