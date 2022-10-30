import time
from . import get_info_api
import settings


def main():
    min = settings.min
    symbol = settings.symbol
    bybit = get_info_api.api(min, symbol)
    mysql = get_info_api.mysql_api()
    # # BybitのBTCUSDTレバレッジ取引のohlcvを取得
    # スタートタイムを将来的にはAPIからの取得を目指す
    start_time = int(time.time()) - (min * 60)
    df = bybit.bybit_get_ohlcv(start_time)
    mysql.insert_db(df, table = "ohlcv")

if __name__ == "__main__":
    main()