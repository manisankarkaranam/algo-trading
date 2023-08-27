import os
from config import Config
import pandas as pd
import utils
from tqdm import tqdm
import logging as log


class DownloadHisData:
    """
    date: date till which data should be downloaded
    stock_symbols_file: File that contains symbols of stocks to be downloaded
    candle_length: Candle Stick length, day-d, week-wk, month-m
    """

    def __init__(self, date, stock_symbols_file, candle_length='d'):
        self.cur_epoch = utils.get_cur_epoch()
        self.download_dir = Config.STOCKS_DOWNLOAD_DIR.format(date=date)
        self.stock_symbols_file_path = Config.STOCK_SYMBOLS_CSV.format(file_name=stock_symbols_file)
        self.candle_length = candle_length

    def check_file_present(self):
        if not os.path.exists(self.stock_symbols_file_path):
            log.error(f"File do not exist {self.stock_symbols_file_path}\nExiting.")
            exit(1)
        if not os.path.exists(Config.STOCKS_HIS_DATA_DIR):
            os.mkdir(Config.STOCKS_HIS_DATA_DIR)

        if not os.path.exists(self.download_dir):
            os.mkdir(self.download_dir)

    def download_data(self):
        self.check_file_present()
        log.debug(f"Saving historical data at: {self.download_dir}\n")
        stock_symbols = pd.read_csv(self.stock_symbols_file_path)
        for stock in tqdm(stock_symbols['Symbol'].to_list()):
            url = Config.HIS_DATA_FETCH_URL.format(stock=stock, epoch=self.cur_epoch, candle_length=self.candle_length)
            try:
                save_path = os.path.join(self.download_dir, f"{stock}.csv")
                utils.download_file(url, save_path)
                log.debug(f"{stock}. Saved")
            except:
                log.error(f"Failed to download {url}")


# if __name__ == "__main__":
#     log.basicConfig()
#     log.getLogger().setLevel(log.INFO)
#
#     downloadHisData = DownloadHisData(date=utils.get_cur_date(),
#                                       stock_symbols_file=Config.STOCKS_ALGO_ABOVE_MA_CSV)
#     downloadHisData.download_data()