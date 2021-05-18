import os
import pickle
import socket
import sys
import threading
import time
import client_menus

HOST = input("Please specify the IP Address of the server ")
PORT = 50000


class RecieveThread(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        while 1:
            message_recu = self.conn.recv(2048).decode("Utf8")
            if "Please be patient for the next session" in message_recu:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(message_recu)
                print("Press Enter to continue")
            if "You may now interact with your interface" in message_recu:
                print(message_recu)
                time.sleep(3)
                th_send.start()
            if not message_recu or message_recu.upper() == "[SERVER]:END":
                break
        th_send._stop()
        print("Client stopped, connection interrupted")
        self.conn.close()


class SendThread(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        choice = "0"
        while choice != "":
            #os.system('cls' if os.name == 'nt' else 'clear')
            client_menus.main_menu()
            choice = input()
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


connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
