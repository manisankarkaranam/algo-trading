import os
from config import Config
import pandas as pd
import utils
from tqdm import tqdm
import logging as log


class DownloadHisData:
    def __init__(self, date):
        self.cur_epoch = utils.get_cur_epoch()
        self.download_dir = Config.STOCKS_DOWNLOAD_DIR.format(date=date)

    def pre_process(self):
        if not os.path.exists(Config.STOCK_SYMBOLS_CSV):
            log.error(f"File do not exist {Config.STOCK_SYMBOLS_CSV}\nExiting")
            exit(1)
        if not os.path.exists(Config.STOCKS_HIS_DATA_DIR):
            os.mkdir(Config.STOCKS_HIS_DATA_DIR)

        if not os.path.exists(self.download_dir):
            os.mkdir(self.download_dir)

    def download_data(self):
        self.pre_process()
        log.info(f"Saving historical data at: {self.download_dir}")
        stock_symbols = pd.read_csv(Config.STOCK_SYMBOLS_CSV)
        for stock in tqdm(stock_symbols['Symbol'].to_list()):
            url = Config.HIS_DATA_FETCH_URL.format(stock=stock, epoch=self.cur_epoch)
            try:
                save_path = os.path.join(self.download_dir, f"{stock}.csv")
                utils.download_file(url, save_path)
                log.debug(f"{stock}. Saved")
            except:
                log.error(f"Failed to download {url}")

# if __name__ == "__main__":
#     downloadHisData = DownloadHisData(date=utils.get_cur_date())
#     downloadHisData.download_data()
