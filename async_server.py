import socket
import sys
import threading
HOST = socket.gethostbyname(socket.gethostname())
PORT = 50000


class ClientThread(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn

    def run(self):
        nom = self.getName()
        while 1:
            msgClient = self.connexion.recv(1024).decode("Utf8")
            if not msgClient or msgClient.upper() == "END":
                break
            message = "%s> %s" % (nom, msgClient)
            print(message)
            for cle in conn_client:
                if cle != nom:
                    conn_client[cle].send(message.encode("Utf8"))
        self.connexion.close()
        del conn_client[nom]
        print(f"Client {nom} disconnected.")


mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    mySocket.bind((HOST, PORT))
except socket.error:
    print("Socket binding error")
    sys.exit()
print(f"Server ready on {HOST}...")
mySocket.listen()
conn_client = {}
while 1:
    connexion, adresse = mySocket.accept()
    th = ClientThread(connexion)
    th.start()
    it = th.getName()
    conn_client[it] = connexion
    print(
        f"Client {it} connected, IP Address {adresse[0]}, port {adresse[1]}.. ")
    # Dialogue avec le client :
    msg = "You are connected, you can send messages..."
    connexion.send(msg.encode("Utf8"))
