import threading
from time import *


class TimerThread(threading.Thread):
    def __init__(self, seconds):
        threading.Thread.__init__(self)
        self.number_of_seconds = seconds
        self.current_time = seconds

    def run(self):
        while self.current_time > 0:
            print(self.current_time)
            self.current_time -= 1
            sleep(1)

    def reset(self):
        self.current_time = self.number_of_seconds
