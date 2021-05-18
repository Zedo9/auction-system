def main_menu():
    print("************Menu******************")
    print("1.Bid for a product")
    print("2.Request a bill")
    print("3.exit")


def bid_for_product_menu():
    data = {"type": "bid"}
    bid = float(input("Bid value=? "))
    data["data"] = bid
    return data
