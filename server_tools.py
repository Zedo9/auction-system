import actions


def main_menu():
    print("**********************Menu******************")
    print("1. Start an auction session for a product")
    print("2. Display current availabe products")
    print("3. Exit")


def brodcast_message(msg, clients_dic):
    msg = "[SERVER]:"+msg
    for client in clients_dic:
        clients_dic[client].send(msg.encode("Utf8"))


def handle_bid_message(msg, sender, th_time, sender_cnx, conn_client):
    # check if data > current_price of product
    # if yes:
    # brodcast the bid
    # update current price
    # update log file
    # reset timer
    # else :
    # send message to sender declining the bid

    print(msg)
    print(sender)
    th_time.reset()


def handle_message(msg, sender, th_time, sender_cnx, conn_client):
    # {type:"bid", data:bid_amount}
    if msg["type"] == "bid":
        handle_bid_message(msg, sender, th_time, sender_cnx, conn_client)
        return
    # {type: "request_bill"}
    if msg["type"] == "request_bill":
        handle_request_bill_message(sender, sender_cnx)
        return


def handle_request_bill_message(sender, sender_cnx):
    client_id = extract_client_id_from_thread_name(sender)
    amount = actions.getClientBill(client_id)
    sender_cnx.send(
        f"You have currently {amount} in your bill".encode("Utf-8"))
    return


def extract_client_id_from_thread_name(thread_name: str):
    return int(thread_name.split("-")[1])
