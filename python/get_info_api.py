import mysql.connector as mysql
import requests
from urllib.error import HTTPError
import pandas as pd
import datetime
import time
from . import settings

# bybit_api
# 引数
# min : 時間 (この間隔で値の取得を行う)
# symbol : シンボル (取得するシンボル)

class api:
    def __init__(self, min, symbol):
        self.min = min
        self.symbol = symbol
        self.limmit = 200
        
    def requests_get(self, url_items, item_data): 
        try:
            response = requests.get(url_items, item_data)
            response.raise_for_status()
            print(response.status_code)
        except HTTPError as e:
            print("error : ", e)
        response_data = response.json()
        return response_data

    # 引数
    # start_time : 取得開始時刻
    # 返値
    # return {"open_time", "op", "hi", "lo", "cl", "volume"}を持つDataFrame型
    
    def bybit_get_ohlcv(self, start_time):
        url_items = 'https://api.bybit.com/public/linear/kline'
        item_data = {
            'symbol' : self.symbol,
            'interval' :self.min,
            'limit' : self.limmit,
            'from' : start_time
        }
        ohlcv = self.requests_get(url_items, item_data)['result']
        if ohlcv is None:
            return 1
        df = pd.DataFrame(ohlcv)[["open_time", "open","high","low","close","volume"]]
        df["open_time"] = [str(datetime.datetime.fromtimestamp(i).replace(second = 0)) for i in df["open_time"]]
        df["open"] = df["open"].astype('float32')
        df["high"] = df["high"].astype('float32')
        df["low"] = df["low"].astype('float32')
        df["close"] = df["close"].astype('float32')
        df["volume"] = df["volume"].astype('float32')
        return df
    
    def bybit_get_orderbook(self):
        url_items = 'https://api.bybit.com/v2/public/orderBook/L2'
        item_data = {
            'symbol' : self.symbol,
        }
        orderbook = self.requests_get(url_items, item_data)
        start_time = orderbook["time_now"]
        orderbook = orderbook["result"]
        df = pd.DataFrame(orderbook)
        df["start_time"] = str(datetime.datetime.fromtimestamp(int(float(start_time))).replace(second = 0))
        buy_df = df.query("side == 'Buy'")
        # buy_dict = dict(zip(buy_df["price"], buy_df["size"]))
        sell_df = df.query("side == 'Sell'")
        # sell_dict = dict(zip(sell_df["price"], sell_df["size"]))
        
        return buy_df, sell_df
    
    def bybit_get_openinsert(self, start_time):
        url_items = 'https://api.bybit.com/v2/public/open-interest'
        if self.min < 5:
            min = 5
        else:
            min = self.min
        item_data = {
            'symbol' : self.symbol,
            'period' : str(min) + 'min',
            'limit' : self.limmit
        }
        openinsert = self.requests_get(url_items, item_data)
        openinsert = openinsert["result"]
        df = pd.DataFrame(openinsert)
        return df
    
    
    
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