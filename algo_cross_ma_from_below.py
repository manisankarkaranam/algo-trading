import pandas as pd
import utils
from config import Config
from datetime import datetime
import logging as log
import pandas_ta as ta
from algorithms_base import AlgorithmsBase

CONSIDER_SLOPE = True
EXPECTED_RETURNS = 7
MOVING_AVERAGE_PERIOD = 200
ROLLING_SLOPE_WINDOW = 30
MAX_HOLD = 90
MAX_LOSS = -100


def entry_check(df, day_index):
    return df.iloc[day_index - 1]["Close"] < df.iloc[day_index - 1]["Moving Average"] and \
        df.iloc[day_index]["Close"] >= df.iloc[day_index]["Moving Average"]


class CrossMAFromBelow(AlgorithmsBase):
    stocks_list_for_algo = Config.STOCKS_ALGO_CROSS_MA_FROM_BELOW_CSV
    result_csv_for_algo = Config.TRADES_CROSS_MA_FROM_BELOW

    def __init__(self, stock_code, data_path):
        self.stock_code = stock_code
        self.data_path = data_path

    def __pre_process_data(self):
        log.info(f"Reading data from path {self.data_path}")
        df = pd.read_csv(self.data_path)
        df = df[["Date", "Close"]].dropna()
        return df

    def __start_back_testing_util(self, df):
        trade_count = 1
        trades_summary = []
        for i in range(1, df.shape[0]):
            if CONSIDER_SLOPE and df.iloc[i]['Slope'] > 0.8 * ROLLING_SLOPE_WINDOW:
                continue
            # Entering trade if today's price moves above moving average
            if entry_check(df, i):
                log.debug(f"\n{trade_count}. Trade entered on {df.iloc[i]['Date']}")
                is_entered = True
                trade_count += 1
                days_in_trade, cur_profit_loss, cur_profit_loss_percent = 0, 0, 0
                for j in range(i + 1, df.shape[0]):
                    days_in_trade = (datetime.strptime(df.iloc[j]['Date'], '%Y-%m-%d') -
                                     datetime.strptime(df.iloc[i]['Date'], '%Y-%m-%d')).days
                    cur_profit_loss = round(df.iloc[j]["Close"] - df.iloc[i]["Close"], 2)
                    cur_profit_loss_percent = round((cur_profit_loss / df.iloc[i]["Close"]) * 100, 2)

                    if days_in_trade >= MAX_HOLD or cur_profit_loss_percent < MAX_LOSS \
                            or cur_profit_loss_percent > EXPECTED_RETURNS:
                        log.debug(f"Entry price: {df.iloc[i]['Close']}")
                        log.debug(f"Entry price: {df.iloc[j]['Close']}")
                        log.debug(f"Trade exited on {df.iloc[j]['Date']} with {cur_profit_loss_percent}% returns "
                                  f"in {days_in_trade} days")

                        is_entered = False
                        break

                if not is_entered:
                    trades_summary.append((self.stock_code, df.iloc[i]['Date'], df.iloc[i]['Close'],
                                           df.iloc[j]['Date'], df.iloc[j]['Close'],
                                           cur_profit_loss, cur_profit_loss_percent, days_in_trade))
                else:
                    log.debug("Could not exit..")
        return trades_summary

    def start_back_testing(self):
        trades_summary = []
        try:
            df = self.__pre_process_data()
            df['Moving Average'] = utils.get_moving_average(df['Close'], MOVING_AVERAGE_PERIOD)
            df = df.dropna()
            if Config.IS_PLOT_NEEDED:
                utils.plot_price_with_moving_avg(df)

            df['Slope'] = utils.get_rolling_slope(df['Moving Average'], window=ROLLING_SLOPE_WINDOW)
            trades_summary = self.__start_back_testing_util(df)
        except:
            log.error(f"Algorithm failed to generate report for {self.stock_code}")
        return trades_summary

    def check_for_trades(self):
        df = self.__pre_process_data()
        df['Moving Average'] = utils.get_moving_average(df['Close'], MOVING_AVERAGE_PERIOD)
        df['Slope'] = utils.get_rolling_slope(df['Moving Average'], window=ROLLING_SLOPE_WINDOW)
        day_index = df.shape[0] - 1
        log.info(f"Checking {self.stock_code}. Yesterday's Close: {df.iloc[day_index - 1]['Close']}, "
                 f"Mov Avg: {df.iloc[day_index]['Moving Average']} "
                 f"Today's Close: {df.iloc[day_index]['Close']}")
        if df.iloc[day_index]['Close'] <= df.iloc[day_index]['Moving Average']:
            log.info(f"Closing Price less than moving average. Keep watching.")
        if entry_check(df, day_index) and df.iloc[day_index]['Slope'] < 0.8 * ROLLING_SLOPE_WINDOW:
            log.info(f"Get Ready. {self.stock_code} can be entered.\n")
            return True
        else:
            log.info(f"Sit Quiet. {self.stock_code} can not be entered.\n")
            return False

# if __name__ == "__main__":
#     log.basicConfig()
#     log.getLogger().setLevel(log.DEBUG)
#     path = f"E:\Algo Trading\Trail1-ML\Scripts\Resources\Stocks-Data\\2023-08-12\ASIANPAINT.csv"
#     algorithm = AlgoAboveMovingAvg("ASIAN", path)
#     algorithm.check_for_trades()
#     algorithm.run_algorithm()
