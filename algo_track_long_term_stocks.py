import pandas as pd
from config import Config
import logging as log
import pandas_ta as ta
from algorithms_base import AlgorithmsBase

MA_PERIOD = 200
RSI_BOTTOM_THRESHOLD = 32


class TrackLongTermStocks(AlgorithmsBase):
    stocks_list_for_algo = Config.STOCKS_ALGO_TRACK_LONG_TERM
    result_csv_for_algo = Config.TRADES_TRACK_LONG_TERM

    def __init__(self, stock_code, data_path):
        self.stock_code = stock_code
        self.data_path = data_path

    def __pre_process_data(self):
        df = pd.read_csv(self.data_path)
        df = df[["Date", "Close"]].dropna()
        df['sma200'] = ta.ma("sma", df['Close'], length=MA_PERIOD).tolist()
        df['rsi'] = ta.rsi(df['Close']).tolist()
        df = df.dropna().reset_index(drop=True)
        return df

    def start_back_testing(self):
        pass

    def check_for_trades(self):
        df = self.__pre_process_data()
        day_index = df.shape[0] - 1
        log.debug(f"Checking {self.stock_code}. Today's Close: {df.loc[day_index]['Close']} "
                  f"SMA: {df.loc[day_index]['sma200']} RSI: {df.loc[day_index]['rsi']}")
        if df.loc[day_index]['Close'] <= df.loc[day_index]['sma200']:
            log.info(f"{self.stock_code} Closing Price less than moving average. Keep watching.")

        last_index = df.index[(df['Close'] < df['sma200']) & (df['rsi'] < RSI_BOTTOM_THRESHOLD)].tolist()[-1]
        if last_index == day_index:
            log.debug(f"=====> {self.stock_code} can be entered. <=====")
            return True
        else:
            log.debug(f"Sit Quiet. {self.stock_code} can not be entered.")
            return False

# if __name__ == "__main__":
#     log.basicConfig()
#     log.getLogger().setLevel(log.DEBUG)
#     path = f"E:\\Algo Trading\\algo-trading\\Resources\\Stocks-Data\\nifty-500\\ASIANPAINT.csv"
#     algorithm = TrackLongTermStocks("ASIAN", path)
#     algorithm.check_for_trades()
