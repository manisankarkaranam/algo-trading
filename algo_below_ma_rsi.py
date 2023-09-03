import pandas as pd
from config import Config
from datetime import datetime
import logging as log
import pandas_ta as ta
from algorithms_base import AlgorithmsBase

MA_PERIOD = 200
EXPECTED_RETURNS = 30
MAX_HOLDING_PERIOD = 200
RSI_BOTTOM_THRESHOLD = 32
MAX_LOSS = -30


class BelowMARSI(AlgorithmsBase):
    stocks_list_for_algo = Config.STOCKS_ALGO_BELOW_MA_RSI
    result_csv_for_algo = Config.TRADES_BELOW_MA_RSI

    def __init__(self, stock_code, data_path):
        self.stock_code = stock_code
        self.data_path = data_path

    def __pre_process_data(self):
        log.debug(f"Reading data from path {self.data_path}")

        df = pd.read_csv(self.data_path)
        df = df[["Date", "Close"]].dropna()
        df['sma200'] = ta.ma("sma", df['Close'], length=MA_PERIOD).tolist()
        df['rsi'] = ta.rsi(df['Close']).tolist()
        df = df[df['Date'] >= '2011-00-00']
        df = df.dropna().reset_index(drop=True)
        return df

    def __start_back_testing_util(self, df):
        trade_count = 1
        trades_summary = []
        previous_exit = '1800-00-00'

        entry_indices = df.index[(df['Close'] < df['sma200']) & (df['rsi'] < RSI_BOTTOM_THRESHOLD)].tolist()
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

                    if (cur_profit_loss_percent > EXPECTED_RETURNS or days_in_trade > MAX_HOLDING_PERIOD or
                            cur_profit_loss_percent <= MAX_LOSS):
                        is_exited = True
                        break
                    next_day += 1

                # 2nd condition is just to ignore invalid data
                if is_exited and cur_profit_loss_percent < 50:
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
                  f"SMA: {df.loc[day_index]['sma200']} RSI: {df.loc[day_index]['rsi']}")
        if df.loc[day_index]['Close'] <= df.loc[day_index]['sma200']:
            log.info(f"{self.stock_code} Closing Price less than moving average. Keep watching.")

        last_index = df.index[(df['Close'] < df['sma200']) & (df['rsi'] < RSI_BOTTOM_THRESHOLD)].tolist()[-1]
        if last_index == day_index:
            log.info(f"=====> {self.stock_code} can be entered. <=====")
            return True
        else:
            log.debug(f"Sit Quiet. {self.stock_code} can not be entered.")
            return False
