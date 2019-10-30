from datetime import datetime, timedelta
import threading
from scraper4 import main

now = datetime.now()
START_TIME = "2019-10-04 00:00:00"
MOCK_START_TIME = "2019-10-03 20:36:00"
run_at = datetime.strptime(MOCK_START_TIME, "%Y-%m-%d %H:%M:%S")

delay = (run_at - now).total_seconds()

threading.Timer(delay, main).start()
