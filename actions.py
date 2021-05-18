import os, threading, time

############ Processing Bien.txt ############
def bienMenuAnnouncmentItems():     # creates a menu for the Server to choose the Product to sell
    with open("Data/bien.txt", 'r') as fRead:
        lines = fRead.readlines()
    available = list()
    for line in lines:
        item = line.split('\t')
        if item[3].lower()=="disponible":
            available.append(item[0])
    # menu
    print("**************************")
    print("Available items for selling")
    print('\n'.join(available))
    print("**************************")    
        
def getInfoProduct(idProduct):      # returns a list of all informations: [prix  de  départ,  dernier  prix,  état et l’identificateur de son acheteur s’il est vendu]
    with open("Data/bien.txt", 'r') as fRead:
        line = [element.rstrip().split('\t')
                for element in fRead.readlines()
                if element.split('\t')[0] == str(idProduct) and element.split('\t')[3] == "vendu"]    # returns a list of one list
    try:
        line[0].remove("vendu")
        return line[0]
    except:
        return [str(idProduct), '0', '0', '0']
    
def changeProductStatus(idProduct):  # change the ETAT of the product in bien.txt from dispo to vendu
    STATUS = "vendu"
    newFileLines = list()
    with open("Data/bien.txt", 'r') as fRead:   # reading
        lines = fRead.readlines()
    for line in lines:                          # processing
        line = line.split('\t')
        if line[0] == str(idProduct):
            line[3] = STATUS
        line = '\t'.join(line)
        newFileLines.append(line)
    with open("Data/bien.txt", 'w') as fWrite:  # writing
        fWrite.writelines(newFileLines)

def changeBuyerID(idProduct, idClient):    # change the buyer ID in bien.txt from 0 to Client ID of the buyer
    newFileLines = list()
    with open("Data/bien.txt", 'r') as fRead:   # reading
        lines = fRead.readlines()
    for line in lines:                          # processing
        line = line.split('\t')
        if line[0] == str(idProduct):
            line[-1] = str(idClient) + '\n'
        line = '\t'.join(line)
        newFileLines.append(line)
    with open("Data/bien.txt", 'w') as fWrite:  # writing
        fWrite.writelines(newFileLines)

############ Processing Histo_bien.txt ############
def createHistoProduct(idProduct):  # creates a Histo file of a product if it doesn't exist
    if not os.path.exists(f"Data/histo/histo_bien{idProduct}.txt"):
        fWrite = open(f"Data/histo/histo_bien{idProduct}.txt", 'w')
        fWrite.close()
        
def addClientRequestToHistoProduct(idProduct, idClient, price):    # add a Client to a request line without STATUS
    fWrite = open(f"Data/histo/histo_bien{idProduct}.txt", 'a')
    fWrite.write(f"{idClient}\t{price}\t")
    fWrite.close()
    
def addProductRequestStatus(idProduct, STATUS): # add a STATUS to a request line in Histo
    fWrite = open(f"Data/histo/histo_bien{idProduct}.txt", 'a')
    fWrite.write(f"\t{STATUS}\n")
    fWrite.close()

def getHistoProduct(idProduct):     # get the histo of a given product
    msg = f"this is the log file for the product {idProduct}:\n"
    try:
        with open(f"Data/histo/histo_bien{idProduct}.txt", 'r') as fRead:
            content = fRead.read()
        return msg + content
    except:
        return f"the log file for the product {idProduct} does not exist!"
  
def LastPrice(idProduct):   # returns last price of a product
    with open(f"Data/histo/histo_bien{idProduct}.txt", 'r') as fRead:
        if fRead.read() == "":
            return getInfoProduct(idProduct)[1]
        else:
            fRead.seek(0)
            lastLine = fRead.readlines()[-1]
            lineElements = lastLine.split('\t')
            return lineElements[1]


############ Processing Facture.txt ############
def addClientToBill(id):     # add a client to Facture with initialization
    with open("Data/facture.txt", 'a') as fAppend:
        fAppend.write(f"\n{str(id)}\t0")
        
def addAmountToBill(idBuyer, price):    # modify the client sum price in facture.txt from 0 to somme a payer
    newFileLines = list()
    with open("Data/facture.txt", 'r') as fRead:   # reading
        lines = fRead.readlines()
    for line in lines:                          # processing
        line = line.split('\t')
        if line[0] == str(idBuyer):
            amount = float(line[-1])
            amount += float(price) * 1.2     # sum = price + price*20%
            line[-1] = str(amount) + '\n'
        line = '\t'.join(line)
        newFileLines.append(line)
    with open("Data/facture.txt", 'w') as fWrite:  # writing
        fWrite.writelines(newFileLines)
               
def getClientBill(idClient):    # return a STRING message about factur
    with open("Data/facture.txt", 'r') as fRead:   # reading
        line = [element.rstrip()
                for element in fRead
                if element.split('\t')[0] == str(idClient)]    # returns a list of one element
    return f"The bill of {idClient} Client is:\n{line[0]}"


############ TEST ############

############ Server ############
#bienMenuAnnouncmentItems()     # return null: it prints a menu

#idProduct, startPrice, finalPrice, idBuyer = getInfoProduct(2)     # return a list of 4 items
#print(idProduct, startPrice, finalPrice, idBuyer)

#addClientToBill(4)     # return null: check facture.txt

#createHistoProduct(5)      # return null: check file structure

#addClientRequestToHistoProduct(4, 3, 500)      # return null: check histo file of the product
#addProductRequestStatus(4, "fail")             # return null: check histo file of the product
#addClientRequestToHistoProduct(4, 5, 600)
#addProductRequestStatus(4, "success")

#changeProductStatus(2)     # return null: check bien.txt

#changeBuyerID(1, 4)    # return null: check bien.txt

#addAmountToBill(2, 700)    # return null: check facture.txt

#print(getClientBill(2))    # return string: facture d'un client

#print(getHistoProduct(1))   # return string: histo d'un bien

############ Client ############
#print(getClientBill(2))

"""semaphore = threading.BoundedSemaphore(value=5) #limit the access to the ressource

def access(thread_number):
    print(f"{thread_number} is trying to access!")
    semaphore.acquire()
    print(f"{thread_number} was granted access!")
    time.sleep(10)
    print(f"{thread_number} is now releasing...")
    semaphore.release()

 
for thread_number in range(1, 11):
    t = threading.Thread(target=access, args=(thread_number,))
    t.start()
    time.sleep(1)"""

"""
def accessProducts(thread_number):
    bienMenuAnnouncmentItems()
    getInfoProduct(idProduct)
    changeProductStatus(idProduct)
    changeBuyerID(idProduct, idClient)

def accessHisto(thread_number, idProduct):
    createHistoProduct(idProduct)
    addClientRequestToHistoProduct(idProduct, idClient, price)
    addProductRequestStatus(idProduct, STATUS)
    removeProductRequestStatus(idProduct)
    getHistoProduct(idProduct)
    
def accessBill(thread_number):
    addClientToBill(id)
    addAmountToBill(idBuyer, price)
"""   

#### CLIENT SIDE ####
"""idClients = ['1', '2', '3', '4', '5']  # get the client id from connections
semaphore_clients = threading.BoundedSemaphore(value=2)  #value=len(idClients)-1

def accessBillClient(idClient):    # CLIENT can do only this function!!
    print(f"Client {idClient} is trying to access!")
    semaphore_clients.acquire()
    print(f"Client {idClient} was granted access!")
    print("**************************")                    ###############
    print(f"{getClientBill(idClient)}")               # the menu that will #
    print("**************************")               # be sended to the client #
    print(f"Client {idClient} is now releasing...")
    time.sleep(1)
    semaphore_clients.release()
    
for idClient in idClients:
    t = threading.Thread(target=accessBillClient, args=(idClient,))
    t.start()
    time.sleep(1)"""
 
#### Server Side ####
# initializing
clientList = ['1', '2', '3', '4', '5']  # Client ID List
spectacleList = ['6', '7', '8', '9']    # Clients connected after 30 sec
# add a client to facture.txt with 0 dt as amount to pay
semaphore_server = threading.BoundedSemaphore(1)
def accessBillToAddClient(idClient):
    print(f"Server is trying to add Client {idClient}!")
    semaphore_server.acquire()
    print(f"Adding Client {idClient}!")
    addClientToBill(idClient)
    print(f"Server is now releasing from adding Client {idClient}...")
    time.sleep(1)
    semaphore_server.release()

for idClient in clientList:
    t = threading.Thread(target=accessBillToAddClient, args=(idClient,))
    t.start()
    time.sleep(1)
# send to the client that he's been added
########### CLIENTS ADDED ###########

# blocking spectacleList from interacting until the session is over
# STARTING the Auction
print("Session starting after ", end='')
i = 10
while i != 0:
    print(f"{str(i)} sec", end='...\n')
    i -= 1
print("*******************")
print("Session STARTED!")
print("*******************")
# a message sent to client telling them that the session has started
########### SESSION STARTED ###########

# print the menu of the available products by accessing bien.txt
semaphore_menu = threading.BoundedSemaphore(1)
def accessProductsMenu():
    print("Server trying to access available Products!")
    semaphore_menu.acquire()
    print("Access granted!")
    bienMenuAnnouncmentItems()
    print("Server is now releasing menu...")
    time.sleep(1)
    semaphore_menu.release()
thread_menu = threading.Thread(target=accessProductsMenu)
thread_menu.start()
time.sleep(1)
# server will choose the product
productID = input('Select product id: ')
# create histo_product.txt if it doesn't exist
lock = threading.Lock()
def accessHistoProduct():
    global lock
    lock.acquire()
    print("***************************************")
    if not os.path.exists(f"Data/histo/histo_bien{productID}.txt"):
        createHistoProduct(productID)
        print(f"histo_bient{productID}.txt has been created!")
    else:
        print("the file is already their!")
    print("*************************")
    lock.release()

thread_lock = threading.Thread(target=accessHistoProduct)
thread_lock.start()
print("****************")
print("Auction Started!")
# a message sent to all clients telling them that the Auction is starting
########### AUCTION STARTED ###########

# Clients will begin to input their prices
############ TIMER ############
def countdown():
    global timer
    timer = 30
    for sec in range(timer):
        timer -= 1
        time.sleep(1)
    if timer == 0:
        print("Out of time!")
countdown_thread = threading.Thread(target=countdown)
countdown_thread.start()
    
# ADD the price to the histo_product.txt
semaphore_histo_price = threading.BoundedSemaphore(1)
def accessHistoProductPrice(idProduct, idClient, price):
    global sugg
    print(f"Client {idClient} is trying to confirm his price!")
    semaphore_histo_price.acquire()
    print("Access granted!")
    if float(price) > float(LastPrice(idProduct)):
        addClientRequestToHistoProduct(idProduct, idClient, price)
        sugg += 1
    print(f"Client {idClient} is now releasing histo_bien{idProduct}...")
    time.sleep(1)
    semaphore_histo_price.release()
    
semaphore_histo_status = threading.BoundedSemaphore(1)
def accessHistoProductStatus():
    global sugg, clientPricesList
    if clientPricesList[-1] == clientPricesList[sugg]:
        addProductRequestStatus(productID, "success")
    else:
        addProductRequestStatus(productID, "fail")

# get the price list from every Client with their id
clientPricesList = [('1','450'), ('2','560'), ('5','580'), ('4','1200'), ('3','700'), ('1','1250'), ('2','1000')]      # kol mayekteb client prix na3mloulou append lel list de tuple hedhi
sugg = 0
while timer > 0 and sugg < len(clientPricesList):
    print("***************")
    thread_client = threading.Thread(target=accessHistoProductPrice, args=(productID, clientPricesList[sugg][0], clientPricesList[sugg][1]))
    thread_client.start()
    lock_request = threading.Lock()
    lock_request.acquire()
    accessHistoProductStatus()
    lock_request.release()
    if len(clientPricesList)-1 == sugg:
        accessHistoProductStatus()
        time.wait(2)
    timer = 30
    
print("Time is up!")