from os import curdir
import threading
from time import *


class TimerThread(threading.Thread):
    def __init__(self, seconds, conn_client, brodcast_function):
        threading.Thread.__init__(self)
        self.number_of_seconds = seconds
        self.current_time = seconds
        self.conn_client = conn_client
        self.brodcast_function = brodcast_function

    def run(self):
        while self.current_time > 0:
            print(self.current_time)
            if (self.current_time == 20 or self.current_time == 10):
                self.brodcast_function(
                    f"{self.current_time} seconds remaining!", self.conn_client)
            self.current_time -= 1
            sleep(1)

    def reset(self):
        self.current_time = self.number_of_seconds
