import os

############ Processing Bien.txt ############


def bienMenuAnnouncmentItems():     # creates a menu for the Server to choose the Product to sell
    with open("Data/bien.txt", 'r') as fRead:
        lines = fRead.readlines()
    available = list()
    for line in lines:
        item = line.split('\t')
        if item[3].lower() == "disponible":
            available.append(item[0])
    # menu
    print("**************************")
    print("Available items for selling")
    print('\n'.join(available))
    print("**************************")


# returns a list of all informations: [prix  de  départ,  dernier  prix,  état et l’identificateur de son acheteur s’il est vendu]
def getInfoProduct(idProduct):
    with open("Data/bien.txt", 'r') as fRead:
        line = [element.rstrip().split('\t')
                for element in fRead.readlines()
                if element.split('\t')[0] == str(idProduct) and element.split('\t')[3] == "vendu"]    # returns a list of one list
    try:
        line[0].remove("vendu")
        return line[0]
    except:
        return [str(idProduct), '0', '0', '0']


# change the ETAT of the product in bien.txt from dispo to vendu
def changeProductStatus(idProduct):
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


# change the buyer ID in bien.txt from 0 to Client ID of the buyer
def changeBuyerID(idProduct, idClient):
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


# creates a Histo file of a product if it doesn't exist
def createHistoProduct(idProduct):
    if not os.path.exists(f"Data/histo/histo_bien{idProduct}.txt"):
        fWrite = open(f"Data/histo/histo_bien{idProduct}.txt", 'w')
        fWrite.close()


# add a Client to a request line without STATUS
def addClientRequestToHistoProduct(idProduct, idClient, price):
    fWrite = open(f"Data/histo/histo_bien{idProduct}.txt", 'a')
    fWrite.write(f"{idClient}\t{price}\t")
    fWrite.close()


# add a STATUS to a request line in Histo
def addProductRequestStatus(idProduct, STATUS):
    fWrite = open(f"Data/histo/histo_bien{idProduct}.txt", 'a')
    fWrite.write(f"{STATUS}\n")
    fWrite.close()


def getHistoProduct(idProduct):     # get the histo of a given product
    msg = f"this is the log file for the product {idProduct}:\n"
    try:
        with open(f"Data/histo/histo_bien{idProduct}.txt", 'r') as fRead:
            content = fRead.read()
        return msg + content
    except:
        return f"the log file for the product {idProduct} does not exist!"


"""    
def LastPrice(idProduct):   # returns last price of a product
    with open(f"Data/histo/histo_bien{idProduct}.txt", 'r') as fRead:
        lastLine = fRead.readlines()[-1]
        lineElements = lastLine.split('\t')
        return lineElements[1]
"""

############ Processing Facture.txt ############


def addClientToBill(id):     # add a client to Facture with initialization
    with open("Data/facture.txt", 'a') as fAppend:
        fAppend.write(f"\n{str(id)}\t0")


# modify the client sum price in facture.txt from 0 to somme a payer
def addAmountToBill(idBuyer, price):
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
    # return f"The bill of {idClient} Client is:\n{line[0]}"
    return line[0]


############ TEST ############

############ Server ############
# bienMenuAnnouncmentItems()     # return null: it prints a menu

# idProduct, startPrice, finalPrice, idBuyer = getInfoProduct(2)     # return a list of 4 items
#print(idProduct, startPrice, finalPrice, idBuyer)

# addClientToBill(4)     # return null: check facture.txt

# createHistoProduct(5)      # return null: check file structure

# addClientRequestToHistoProduct(4, 3, 500)      # return null: check histo file of the product
# addProductRequestStatus(4, "fail")             # return null: check histo file of the product
#addClientRequestToHistoProduct(4, 5, 600)
#addProductRequestStatus(4, "success")

# changeProductStatus(2)     # return null: check bien.txt

# changeBuyerID(1, 4)    # return null: check bien.txt

# addAmountToBill(2, 700)    # return null: check facture.txt

# print(getClientBill(2))    # return string: facture d'un client

# print(getHistoProduct(1))   # return string: histo d'un bien

############ Client ############
# print(getClientBill(2))
