from datetime import date
import time
from urllib.request import urlopen
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
