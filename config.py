import os


class Config:
    # Paths
    BASE_DIR = os.getcwd()
    RESOURCE_DIR = os.path.join(BASE_DIR, 'Resources')
    STOCK_SYMBOLS_CSV = os.path.join(RESOURCE_DIR, 'stock-considered.csv')
    STOCKS_HIS_DATA_DIR = os.path.join(RESOURCE_DIR, 'Stocks-Data')
    STOCKS_DOWNLOAD_DIR = os.path.join(STOCKS_HIS_DATA_DIR, '{date}')
    RESULTS_DIR = os.path.join(BASE_DIR, 'Results')

    # Urls
    HIS_DATA_FETCH_URL = "https://query1.finance.yahoo.com/v7/finance/download/" \
                         "{stock}.NS?period1=946684800&period2={epoch}&interval=1d&" \
                         "events=history&includeAdjustedClose=true"

    # Configurations
    IS_PLOT_NEEDED = False
