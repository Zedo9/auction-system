import actions, time


def main_menu():
    print("**********************Menu******************")
    print("1. Start an auction session for a product")
    print("2. Display current availabe products")
    print("3. Exit")


def brodcast_message(msg, clients_dic):
    msg = "[SERVER]:"+msg
    for client in clients_dic:
        clients_dic[client].send(msg.encode("Utf8"))


def handle_bid_message(msg, sender, th_time, sender_cnx, conn_client, LOCKS):
    LOCKS["bien"].acquire()
    client_id = extract_client_id_from_thread_name(sender)
    new_price = msg["data"]
    price = actions.getInfoProduct(msg["current_product"])[2]
    LOCKS["bien"].release()
    if float(new_price) <= float(price):
        sender_cnx.send(f"Your bid value is less than the current price".encode("Utf-8"))
    else :
        brodcast_message(f"NEW BID : {sender} made a bid with {new_price}!", conn_client)
        LOCKS["bien"].acquire()
        actions.updateCurrentPrice(msg["current_product"], new_price)
        LOCKS["bien"].release()
        LOCKS["log"].acquire()
        actions.addClientRequestToHistoProduct(msg["current_product"], client_id, new_price)
        actions.addProductRequestStatus(msg["current_product"], "fail")
        LOCKS["log"].release()
        th_time.reset()

def handle_finish_session(conn_client, current_product):
    try:
        client_id, amount = actions.replaceStatusToSuccess(current_product)
        actions.changeBuyerID(current_product, client_id)
        actions.addAmountToBill(client_id,amount)
        brodcast_message(f"{extract_client_id_from_thread_name(client_id)} has acquired product {current_product} for {amount} Dinars",conn_client)
    except:
        pass

def handle_message(msg, sender, th_time, sender_cnx, conn_client, LOCKS):
    # {type:"bid", data:bid_amount}
    if msg["type"] == "bid":
        handle_bid_message(msg, sender, th_time, sender_cnx, conn_client, LOCKS)
    # {type: "request_bill"}
    if msg["type"] == "request_bill":
        handle_request_bill_message(sender, sender_cnx, LOCKS)


def handle_request_bill_message(sender, sender_cnx, LOCKS):
    client_id = extract_client_id_from_thread_name(sender)
    LOCKS["facture"].acquire()
    amount = actions.getClientBill(client_id)
    LOCKS["facture"].release()
    sender_cnx.send(
        f"You have currently {amount} in your bill".encode("Utf-8"))


def extract_client_id_from_thread_name(thread_name: str):
    return int(thread_name.split("-")[1])
