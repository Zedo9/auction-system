import pickle
import socket
import sys
import threading
from time import sleep
import client_menus

import sys
try :
    protocol = sys.argv[1]
    if protocol.lower() not in ("tcp","udp"):
        print("Please specify the communications protocol <tcp> or <udp>")
        sys.exit()
except:
    protocol = "tcp"
    pass


#HOST = input("Please specify the IP Address of the server ")
#PORT = 50000
HOST = "3.131.207.170"
PORT = 14647


class RecieveThread(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        while 1:
            message_recu = self.conn.recv(2048).decode("Utf8")
            print(message_recu)
            if "You may now sumbit your bids" in message_recu:
                if (th_send.is_alive() != True):
                    th_send.start()
            if "[SERVER]:END" in message_recu:
                break
            if "[SERVER]:Auction Session Ended" in message_recu:
                pass
            if "[SERVER]:NEW BID" in message_recu:
                pass
        th_send._stop()
        print("Client stopped, connection interrupted from server")
        self.conn.close()


class SendThread(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn
        #   self.stoprequest = threading.Event()

    def run(self):
        client_menus.main_menu()
        while True:
            choice = input("Choose an option ")
            if choice == "1":
                data = client_menus.bid_for_product_menu()
                pickled_data = pickle.dumps(data)
                self.conn.send(pickled_data)
            if choice == "2":
                data = {"type": "request_bill"}
                pickled_data = pickle.dumps(data)
                self.conn.send(pickled_data)
            if choice == "3":
                data = {"type": "disconnect"}
                pickled_data = pickle.dumps(data)
                self.conn.send(pickled_data)
                break

    # def join(self, timeout=None):
    #     self.stoprequest.set()
    #     threading.Thread.join(timeout)

PROTOCOLS = {"tcp": socket.SOCK_STREAM, "udp": socket.SOCK_DGRAM}
connection = socket.socket(socket.AF_INET, PROTOCOLS[protocol])
try:
    connection.connect((HOST, PORT))
except socket.error:
    print("Connection Error")
    sys.exit()
print("Connected to the server!")
th_send = SendThread(connection)
th_recieve = RecieveThread(connection)
th_recieve.start()
th_recieve.join()
