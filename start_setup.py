import os
import utils
import shutil
import pandas as pd
import logging as log
from config import Config
from download_his_data import DownloadHisData
from algo_cross_ma_from_below import CrossMAFromBelow
from algo_below_ma_rsi import BelowMARSI


class StartSetup:
    def __init__(self, algorithm_class, start_date, end_date=''):
        self.start_date = start_date
        self.end_date = end_date
        self.cur_date = utils.get_cur_date()
        self.algorithm_class = algorithm_class

    def download_his_data(self, flush):
        log.debug(f"Downloading historical data from file {self.algorithm_class.stocks_list_for_algo}")
        download_his_data_obj = DownloadHisData(self.cur_date, self.algorithm_class.stocks_list_for_algo)

        if flush and os.path.exists(download_his_data_obj.download_dir):
            shutil.rmtree(download_his_data_obj.download_dir)

        download_his_data_obj.download_data()

    def init_setup(self, download=True, flush=True):
        if download:
            self.download_his_data(flush)

    def back_test_all_stocks(self):
        back_tested_data = []
        algorithm = None
        for stock in os.listdir(Config.STOCKS_DOWNLOAD_DIR.format(date=self.cur_date)):
            path = os.path.join(Config.STOCKS_DOWNLOAD_DIR.format(date=self.cur_date), stock)
            algorithm = self.algorithm_class(stock.strip(".csv"), path)
            back_tested_data.extend(algorithm.start_back_testing())
        back_tested_data_df = pd.DataFrame(back_tested_data, columns=['Stock', 'Entry', 'Buy', 'Exit', 'Sell',
                                                                      'ProfitLoss', 'Returns', 'DaysInTheTrade'])
        back_tested_data_df = back_tested_data_df[back_tested_data_df['Entry'] > self.start_date]
        result_file_path = Config.RESULT_CSV.format(file_name=algorithm.result_csv_for_algo)
        back_tested_data_df.to_csv(result_file_path, index=False)
        log.info(f"Result filed saved at {result_file_path}")

    def check_for_trades(self):
        trades_found = []
        for stock in os.listdir(Config.STOCKS_DOWNLOAD_DIR.format(date=self.cur_date)):
            path = os.path.join(Config.STOCKS_DOWNLOAD_DIR.format(date=self.cur_date), stock)
            algorithm = self.algorithm_class(stock.strip(".csv"), path)
            if algorithm.check_for_trades():
                trades_found.append(stock.strip(".csv"))
        if len(trades_found):
            log.info(f"\n##### Voila.. Trades found: {trades_found} #####\n\n")
        else:
            log.info("\n##### Relax macha... No action for today. #####\n\n")


def setup_logger():
    root_logger = log.getLogger()
    root_logger.setLevel(log.DEBUG)

    fh = log.FileHandler('logs.log', mode='w')
    formatter = log.Formatter('%(message)s')
    fh.setFormatter(formatter)
    fh.setLevel(log.DEBUG)
    root_logger.addHandler(fh)

    console_handler = log.StreamHandler()
    console_handler.setLevel(log.INFO)
    root_logger.addHandler(console_handler)


if __name__ == "__main__":
    setup_logger()

    # Running CrossMAFromBelow Algorithm
    log.info("##########################################################################")
    log.info("#####                      Cross MA From Below                       #####")
    log.info("##########################################################################")
    setup_algo_cross_ma_from_below = StartSetup(CrossMAFromBelow, '2001-00-00')
    setup_algo_cross_ma_from_below.init_setup()
    setup_algo_cross_ma_from_below.check_for_trades()
    # setup_algo_cross_ma_from_below.back_test_all_stocks()

    # Running BelowMARSI Algorithm
    log.info("##########################################################################")
    log.info("#####                      Below MA and RSI                          #####")
    log.info("##########################################################################")
    setup_algo_below_ma_rsi = StartSetup(BelowMARSI, '2001-00-00')
    setup_algo_below_ma_rsi.init_setup()
    setup_algo_below_ma_rsi.check_for_trades()
    # setup_algo_below_ma_rsi.back_test_all_stocks()
