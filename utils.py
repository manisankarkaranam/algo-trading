from datetime import date
import time
from urllib.request import urlopen
import numpy as np
import matplotlib.pyplot as plt


def get_cur_date():
    return str(date.today())


def get_cur_epoch():
    return str(int(time.time()))


def download_file(url, save_path):
    # Download from URL
    with urlopen(url) as file:
        content = file.read().decode()
    # Save to file
    with open(save_path, 'w+') as download:
        download.write(content)


def get_moving_average(prices, moving_average_period=200):
    moving_average_prices = [np.nan] * (moving_average_period-1)
    for i in range(moving_average_period, prices.shape[0]+1):
        moving_average_prices.append(np.average(prices[i-moving_average_period:i]))
    return moving_average_prices


def plot_price_with_moving_avg(df):
    plt.figure(figsize=(18, 9))
    plt.plot(range(df.shape[0]), df['Close'], color='blue', label='Close')
    plt.plot(range(df.shape[0]), df['Moving Average'], color='red', label='Moving Average')
    plt.xticks(range(0, df.shape[0], 500), df['Date'].loc[::500], rotation=45)

    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Price', fontsize=18)
    plt.show()


# Counts no of above values(in WINDOW time period) greater than current value. Intention is moving avg should increase
def rolling_window(a, window):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


def get_rolling_slope(data, window=30):
    x = np.concatenate([[np.nan] * window, data.values])
    arr = rolling_window(x, window+1)
    return (arr[:, :-1] > arr[:, [-1]]).sum(axis=1)
