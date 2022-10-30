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
    buy_df, sell_df = bybit.get_orderbook()
    mysql.insert_db(buy_df, table = "orderbook_buy")
    mysql.insert_db(sell_df, table = "orderbook_sell")

if __name__ == "__main__":
    main()