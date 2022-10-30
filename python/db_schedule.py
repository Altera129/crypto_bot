import schedule
from time import sleep
import get_ohlcv_1min
import get_orderbook_1min

def job_1min():
    get_ohlcv_1min.main()
    get_orderbook_1min.main()
    
if __name__ == "__main__":
    schedule.every(1).minutes.do(job_1min)
    
    while True:
        schedule.run_pending()
        sleep(1)
