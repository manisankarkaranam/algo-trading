import pandas as pd
import utils
from config import Config
from datetime import datetime
import logging as log
import pandas_ta as ta
from algorithms_base import AlgorithmsBase

EXPECTED_RETURNS = 7
MA_PERIOD = 100
MAX_HOLD = 90
MAX_LOSS = -100
MAX_RSI = 80
MIN_RSI = 20


def get_entry_indices(df):
    return df.index[(df['pre_close'] < df['sma']) & (df['Close'] >= df['sma']) &
                    (df['rsi'] < MAX_RSI) & (df['rsi'] > MIN_RSI)].tolist()


class CrossMAFromBelow(AlgorithmsBase):
    stocks_list_for_algo = Config.STOCKS_ALGO_CROSS_MA_FROM_BELOW_CSV
    result_csv_for_algo = Config.TRADES_CROSS_MA_FROM_BELOW

    def __init__(self, stock_code, data_path):
        self.stock_code = stock_code
        self.data_path = data_path

    def __pre_process_data(self):
        df = pd.read_csv(self.data_path)
        df = df[["Date", "Close"]].dropna()
        df['sma'] = ta.ma("sma", df['Close'], length=MA_PERIOD).tolist()
        df['rsi'] = ta.rsi(df['Close']).tolist()
        df['pre_close'] = df['Close'].shift(1)
        df = df[df['Date'] >= '2011-00-00']
        df = df.dropna().reset_index(drop=True)
        return df

    def __start_back_testing_util(self, df):
        trade_count = 1
        trades_summary = []
        previous_exit = '1800-00-00'

        entry_indices = get_entry_indices(df)
        for index in entry_indices:
            if df.loc[index]['Date'] > previous_exit:
                log.debug(f"\n{trade_count}. Trade entered on {df.loc[index]['Date']}")
                is_exited = False
                trade_count += 1

                days_in_trade, cur_profit_loss, cur_profit_loss_percent = 0, 0, 0
                next_day = index + 1
                while next_day < df.shape[0]:
                    cur_profit_loss = round(df.loc[next_day]["Close"] - df.loc[index]["Close"], 2)
                    cur_profit_loss_percent = round((cur_profit_loss / df.loc[index]["Close"]) * 100, 2)
                    previous_exit = df.loc[next_day]["Date"]
                    days_in_trade = (datetime.strptime(df.loc[next_day]['Date'], '%Y-%m-%d') -
                                     datetime.strptime(df.loc[index]['Date'], '%Y-%m-%d')).days

                    if (cur_profit_loss_percent >= EXPECTED_RETURNS or
                            days_in_trade > MAX_HOLD or
                            cur_profit_loss_percent <= MAX_LOSS):
                        is_exited = True
                        break

                    next_day += 1

                if is_exited:
                    log.debug(f"Entry price: {df.loc[index]['Close']}")
                    log.debug(f"Exit price: {df.loc[next_day]['Close']}")
                    log.debug(f"Trade exited on {df.loc[next_day]['Date']} with {cur_profit_loss_percent}% returns "
                              f"in {days_in_trade} days")
                    trades_summary.append((self.stock_code, df.loc[index]['Date'], df.loc[index]['Close'],
                                           df.loc[next_day]['Date'], df.loc[next_day]['Close'],
                                           cur_profit_loss, cur_profit_loss_percent, days_in_trade))
                else:
                    log.debug("Could not exit..")
        return trades_summary

    def start_back_testing(self):
        trades_summary = []
        try:
            df = self.__pre_process_data()
            trades_summary = self.__start_back_testing_util(df)
        except:
            log.error(f"Algorithm failed to generate report for {self.stock_code}")
        return trades_summary

    def check_for_trades(self):
        df = self.__pre_process_data()
        day_index = df.shape[0] - 1
        log.debug(f"Checking {self.stock_code}. Today's Close: {df.loc[day_index]['Close']} "
                  f"SMA: {df.loc[day_index]['sma']} RSI: {df.loc[day_index]['rsi']}")
        if df.loc[day_index]['Close'] <= df.loc[day_index]['sma']:
            log.info(f"{self.stock_code} Closing Price less than moving average. Keep watching.")

        last_index = get_entry_indices(df)[-1]
        if last_index == day_index:
            log.info(f"=====> {self.stock_code} can be entered. <=====")
            return True
        else:
            log.debug(f"Sit Quiet. {self.stock_code} can not be entered.")
            return False


# if __name__ == "__main__":
#     log.basicConfig()
#     log.getLogger().setLevel(log.DEBUG)
#     path = f"E:\\Algo Trading\\algo-trading\\Resources\\Stocks-Data\\nifty-500\\ASIANPAINT.csv"
#     algorithm = CrossMAFromBelow("ASIAN", path)
#     algorithm.start_back_testing()
#     algorithm.check_for_trades()

