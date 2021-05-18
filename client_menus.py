def main_menu():
    print("************Menu******************")
    print("1.Bid for current product")
    print("2.Check your bill")
    print("3.Exit")


def bid_for_product_menu():
    data = {"type": "bid"}
    bid = float(input("Bid value=? "))
    data["data"] = bid
    return data
