import datetime
import time
import get_info_api

import settings


def main():
    min = settings.min
    symbol = settings.symbol
    bybit = get_info_api.bybit_api(min, symbol)
    mysql = get_info_api.mysql_api()
    # # BybitのBTCUSDTレバレッジ取引のohlcvを取得
    # スタートタイムを将来的にはAPIからの取得を目指す
    start_time = int(datetime.datetime(2020, 4, 1).timestamp())
    while start_time < int(time.time()):
        df = bybit.get_ohlcv(start_time)
        mysql.insert_db(df, table = "ohlcv")
        start_time += bybit.limmit * (60 * min) # 200=limmit 60=秒数
        
if __name__ == "__main__":
    main()
    