import time
from get_info_api import bybit_api
from get_info_api import mysql_api

import settings


def main():
    min = settings.min
    symbol = settings.symbol
    bybit = bybit_api(min, symbol)
    mysql = mysql_api()
    # # BybitのBTCUSDTレバレッジ取引のohlcvを取得
    # スタートタイムを将来的にはAPIからの取得を目指す
    start_time = int(time.time()) - (min * 60)
    df = bybit.get_ohlcv(start_time)
    mysql.insert_db(df, table = "ohlcv")

if __name__ == "__main__":
    main()