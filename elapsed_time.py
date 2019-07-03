import time
import threading

class ElapsedTimeThread(threading.Thread):
    """"Stoppable thread that prints the time elapsed"""
    def __init__(self, iteration, total, card, row):
        super(ElapsedTimeThread, self).__init__()
        self._stop_event = threading.Event()
        self.iteration = iteration
        self.total = total
        self.card = card
        self.row = row

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        thread_start = time.time()
        while not self.stopped():
            print(f"\r{self.row}".format(self.iteration, self.total, self.card,
                time.time()-thread_start), end="", flush=True)
            time.sleep(0.01)
