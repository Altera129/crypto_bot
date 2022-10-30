import mysql.connector as mysql
from pybit import usdt_perpetual
import pandas as pd
import datetime
import time
import settings

# bybit_api
# 引数
# min : 時間 (この間隔で値の取得を行う)
# symbol : シンボル (取得するシンボル)

class bybit_api:
    def __init__(self, min, symbol):
        self._session = usdt_perpetual.HTTP(
            endpoint='https://api.bybit.com', 
            api_key=settings.api_key,
            api_secret=settings.api_secret
        )

        self._ws = usdt_perpetual.WebSocket(
            test=False,
            api_key=settings.api_key,
            api_secret=settings.api_secret
        )
        self.min = min
        self.symbol = symbol
        self.limmit = 200

    # 引数
    # start_time : 取得開始時刻
    # 返値
    # return {"open_time", "op", "hi", "lo", "cl", "volume"}を持つDataFrame型
    
    def get_ohlcv(self, start_time):
        ohlcv = self._session.query_kline(symbol=self.symbol,
                            interval=self.min,
                            limmit = self.limimt, #将来的には別の場所に保存
                            from_time=start_time)['result']

        df = pd.DataFrame(ohlcv)[["open_time", "open","high","low","close","volume"]]
        df["open_time"] = [str(datetime.datetime.fromtimestamp(i).replace(second = 0)) for i in df["open_time"]]
        df["open"] = df["open"].astype('float32')
        df["high"] = df["high"].astype('float32')
        df["low"] = df["low"].astype('float32')
        df["close"] = df["close"].astype('float32')
        df["volume"] = df["volume"].astype('float32')
        
        return df
    
    def get_orderbook(self):
        session_return = self._session.orderbook(symbol=self.symbol)
        start_time = session_return["time_now"]
        orderbook = session_return["result"]
        df = pd.DataFrame(orderbook)
        df["start_time"] = str(datetime.datetime.fromtimestamp(int(float(start_time))).replace(second = 0))
        buy_df = df.query("side == 'Buy'")
        # buy_dict = dict(zip(buy_df["price"], buy_df["size"]))
        sell_df = df.query("side == 'Sell'")
        # sell_dict = dict(zip(sell_df["price"], sell_df["size"]))
        
        return buy_df, sell_df
    
class mysql_api:
    def __init__(self):
        # 将来的にはdockerで使用予定のenvを読み込む
        self.host="mysql"
        self.port="3306"
        self.user="root"
        self.password="root"
        self.database="btcusdt"
        
    def insert_db(self, df, table):
        connection = mysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
            )
            
        cursor = connection.cursor(buffered=True)
        try:
            insert_sql = "INSERT INTO {table} VALUES (%s".format(table=table)
            for i in range(len(df.columns) - 1):
                insert_sql += ",%s"
            insert_sql += ");"
            
            cursor.executemany(insert_sql, df.values.tolist())
            connection.commit()
            
        except Exception as e:
            print(e) #将来的にはログ、Discordに出力
            return -1
        
        cursor.close()
        connection.close()
        
        return 0