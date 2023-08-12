import os
import utils
import pandas as pd
import logging as log
from config import Config
from download_his_data import DownloadHisData
from algo_above_moving_avg import AlgoAboveMovingAvg


log.basicConfig()
log.getLogger().setLevel(log.INFO)


class StartSetup:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.cur_date = utils.get_cur_date()

    def start_setup(self, download=True):
        if download:
            log.info("Downloading data...")
            download_his_data_obj = DownloadHisData(self.cur_date)
            download_his_data_obj.download_data()
        self.check_for_trades()

    def back_test_all_stocks(self):
        back_tested_data = []
        for stock in os.listdir(Config.STOCKS_DOWNLOAD_DIR.format(date=self.cur_date)):
            path = os.path.join(Config.STOCKS_DOWNLOAD_DIR.format(date=self.cur_date), stock)
            algorithm = AlgoAboveMovingAvg(stock.strip(".csv"), path)
            back_tested_data.extend(algorithm.run_algorithm())
        back_tested_data_df = pd.DataFrame(back_tested_data, columns = ['Stock', 'Entry', 'Buy', 'Exit', 'Sell',
                                                                        'ProfitLoss', 'Returns', 'DaysInTheTrade'])
        back_tested_data_df = back_tested_data_df[back_tested_data_df['Entry'] > self.start_date]
        back_tested_data_df.to_csv("output.csv", index=False)

    def check_for_trades(self):
        trades_found = []
        for stock in os.listdir(Config.STOCKS_DOWNLOAD_DIR.format(date=self.cur_date)):
            path = os.path.join(Config.STOCKS_DOWNLOAD_DIR.format(date=self.cur_date), stock)
            algorithm = AlgoAboveMovingAvg(stock.strip(".csv"), path)
            if algorithm.check_for_trades():
                trades_found.append(stock.strip(".csv"))
        if len(trades_found):
            log.info(f"Voila.. Trades found: {trades_found}")
        else:
            log.info("Relax macha... No action for today.")


if __name__ == "__main__":
    setup_obj = StartSetup('2001-01-01', '')
    setup_obj.start_setup()
    # setup_obj.iterate_all_stocks()
