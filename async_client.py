import socket
import sys
import threading

HOST = input("Please specify the IP Address of the server ")
PORT = 50000


class RecieveThread(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn  # réf. du socket de connexion

    def run(self):
        while 1:
            message_recu = self.conn.recv(1024).decode("Utf8")
            print("*" + message_recu + "*")
            if not message_recu or message_recu.upper() == "END":
                break
        # Le thread <réception> se termine ici.
        # On force la fermeture du thread <émission> :
        th_E._stop()
        print("Client stopped, connection interrupted")
        self.conn.close()


class SendThread(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        while 1:
            message_emis = input()
            self.conn.send(message_emis.encode("Utf8"))


connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    connection.connect((HOST, PORT))
except socket.error:
    print("Connection Error")
    sys.exit()
print("Connected to the server!")
th_E = SendThread(connection)
th_R = RecieveThread(connection)
th_E.start()
th_R.start()
