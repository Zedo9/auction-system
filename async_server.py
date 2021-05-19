import os
from time import sleep
import timer_thread
import server_tools
import socket
import sys
import threading
import pickle
import actions

import sys
try :
    protocol = sys.argv[1]
    if protocol.lower() not in ("tcp","udp"):
        print("Please specify the communications protocol <tcp> or <udp>")
        sys.exit()
except:
    protocol = "tcp"
    pass

HOST = '127.0.0.1'
CLIENTS_MAX = int(input("How many clients will be connecting? "))
CLIENTS_COUNT = 0
PORT = 50000
TIMER = 30
CURRENT_PRODUCT = 0

LOCK_LOG = threading.Lock()
LOCK_BIEN = threading.Lock()
LOCK_FACTURE = threading.Lock()
LOCKS = {"facture": LOCK_FACTURE, "bien": LOCK_BIEN, "log": LOCK_LOG}


class ClientThread(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn
        actions.addClientToBill(
            server_tools.extract_client_id_from_thread_name(self.getName()))

    def run(self):
        nom = self.getName()
        while 1:
            msgClient = b''
            msgClient = self.connexion.recv(2048)
            msgClientDict = pickle.loads(msgClient)
            msgClientDict["current_product"] = CURRENT_PRODUCT
            if msgClientDict["type"] == "disconnect":
                server_tools.handle_request_bill_message(nom,self.connexion, LOCKS)
                break
            server_tools.handle_message(
                msgClientDict, nom, th_time, self.connexion, conn_client, LOCKS)
        self.connexion.close()
        del conn_client[nom]
        print(f"Client {nom} disconnected.")


PROTOCOLS = {"tcp": socket.SOCK_STREAM, "udp": socket.SOCK_DGRAM}
mySocket = socket.socket(socket.AF_INET, PROTOCOLS[protocol])
try:
    mySocket.bind((HOST, PORT))
except socket.error:
    print("Socket binding error")
    sys.exit()
print(f"Server ready on {HOST}")
mySocket.listen()
conn_client = {}
while 1:
    connexion, adresse = mySocket.accept()
    th = ClientThread(connexion)
    th.start()
    it = th.getName()
    CLIENTS_COUNT += 1
    conn_client[it] = connexion
    print(
        f"Client {it} connected, IP Address {adresse[0]}, port {adresse[1]}.. ")
    msg = "Please wait for the auction session to start"
    connexion.send(msg.encode("Utf8"))
    if CLIENTS_COUNT == CLIENTS_MAX:
        break
choice = "0"
while choice != "4":
    # os.system('cls' if os.name == 'nt' else 'clear')
    server_tools.main_menu()
    choice = input()
    if choice == "1":
        CURRENT_PRODUCT = int(input("Product ID? "))
        th_time = timer_thread.TimerThread(
            TIMER, conn_client, server_tools.brodcast_message)
        try:
            product_details = actions.getInfoProduct(CURRENT_PRODUCT)
            if product_details[-2] == "vendu":
                print("This product was already sold")
                continue
            actions.createHistoProduct(CURRENT_PRODUCT)
            server_tools.brodcast_message(
                "Product details" +
                "\n" +
                f"ID : {product_details[0]}" +
                "\n" +
                f"start_price : {product_details[1]}" +
                "\n" +
                "Countdown has started : 30 Seconds remaining" +
                "\n" +
                "You may now sumbit your bids", conn_client)
            th_time.start()
            th_time.join()
            server_tools.brodcast_message(
                f"Auction Session Ended for product {CURRENT_PRODUCT}", conn_client)
            server_tools.handle_finish_session(conn_client, CURRENT_PRODUCT)
        except:
            print("Error fetching product data")
    if choice == "2":
        os.system('cls' if os.name == 'nt' else 'clear')
        actions.bienMenuAnnouncmentItems()
    if choice == "3":
        product_id = int(input("Product ID? "))
        print(actions.getHistoProduct(product_id))
# All products are sold
server_tools.brodcast_message("END", conn_client)
