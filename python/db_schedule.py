import schedule
from time import sleep
from . import get_ohlcv
from . import get_orderbook

def job_1min():
    get_ohlcv.main()
    get_orderbook.main()
    
if __name__ == "__main__":
    schedule.every(1).minutes.do(job_1min)
    
    while True:
        schedule.run_pending()
        sleep(1)
