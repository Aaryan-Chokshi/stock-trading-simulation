from pymongo import MongoClient
def get_database():
    CONNECTION_STRING = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.1.0"
    client = MongoClient(CONNECTION_STRING)
    print("Connection estblished")
    return client['user_shopping_list']

dbname = get_database()
collection_name = dbname["wealth_collection"]

def read_database(id):
    item_details = collection_name.find({"dbid": id})
    for item in item_details:
        print(item)
        pass
    pass

# Onboarding a customer
def add_customer(dbid):
    collection_name.insert_one({"dbid": dbid, "fund": 10000, "shares": []})
    pass

# Buying a share
def buy_share(dbid, share, qty, price):
    item_details = collection_name.find_one({"dbid": dbid})
    fund = item_details["fund"]
    shares = item_details["shares"]
    fund -= qty * price
    for i in range(len(shares)):
        if shares[i]["share"] == share:
            shares[i]["qty"] += qty
            break
        pass
    else:
        shares.append({"share": share, "qty": qty})
    collection_name.update_one({"dbid": dbid}, {"$set": {"shares": shares, "fund": fund}})
    return

# Selling a share
def sell_share(dbid, share, qty, price):
    item_details = collection_name.find_one({"dbid": dbid})
    fund = item_details["fund"]
    shares = item_details["shares"]
    fund += qty * price
    for i in range(len(shares)):
        if shares[i]["share"] == share:
            shares[i]["qty"] -= qty
            break
        pass
    collection_name.update_one({"dbid": dbid}, {"$set": {"shares": shares, "fund": fund}})
    return

# Getting the fund of a customer
def get_fund(dbid):
    item_details = collection_name.find_one({"dbid": dbid})
    return item_details["fund"]

# Getting the shares of a customer
def get_shares(dbid, share):
    item_details = collection_name.find_one({"dbid": dbid})
    shares = item_details["shares"]
    for i in range(len(shares)):
        if shares[i]["share"] == share:
            return shares[i]["qty"]
        pass
    else:
        return 0
    pass

# Getting the wealth of a customer
def get_shares_list(dbid):
    item_details = collection_name.find_one({"dbid": dbid})
    shares = item_details["shares"]
    return shares


add_customer('1')
read_database('1')