import os, threading, time

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
                if element.split('\t')[0] == str(idProduct)]    # returns a list of one list
    return line[0]

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
            line[-2] = "vendu"
        line = '\t'.join(line)
        newFileLines.append(line)
    with open("Data/bien.txt", 'w') as fWrite:  # writing
        fWrite.writelines(newFileLines)
        
# change the final price value
def updateCurrentPrice(idProduct, price):
    newFileLines = list()
    with open("Data/bien.txt", 'r') as fRead:   # reading
        lines = fRead.readlines()
    for line in lines:                          # processing
        line = line.split('\t')
        if line[0] == str(idProduct):
            line[2] = str(price)
        line = '\t'.join(line)
        newFileLines.append(line)
    with open("Data/bien.txt", 'w') as fWrite:  # writing
        fWrite.writelines(newFileLines)
# test
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

# replace final status to success and return the (buyer ID, final price)
def replaceStatusToSuccess(idProduct):
    with open(f"Data/histo/histo_bien{idProduct}.txt", 'r') as fRead:   # reading
        lines = fRead.readlines()
    ch = lines[-1].replace("fail", "success")
    lines.remove(lines[-1])
    lines.append(ch)
    with open(f"Data/histo/histo_bien{idProduct}.txt", 'w') as fWrite:  # writing
        fWrite.writelines(lines)
    return ch.split('\t')[0], ch.split('\t')[1]
    
# add a STATUS to a request line in Histo
def addProductRequestStatus(idProduct, STATUS):
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
    with open("Data/facture.txt", 'r') as fRead:   # reading
        lines = fRead.readlines()
    add = True
    for line in lines:                          # processing
        line = line.split('\t')
        if line[0] == str(id):
            add = False
    if add:
        with open("Data/facture.txt", 'a') as fAppend:
            fAppend.write(f"{str(id)}\t0\n")


# modify the client sum price in facture.txt from 0 to somme a payer
def addAmountToBill(idBuyer, price):
    newFileLines = list()
    with open("Data/facture.txt", 'r') as fRead:   # reading
        lines = fRead.readlines()
    for line in lines:                          # processing
        line = line.split('\t')
        if line[0] == str(idBuyer):
            old = float(line[-1])
            amount = old
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
