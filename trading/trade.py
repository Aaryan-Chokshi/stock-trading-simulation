from flask import Flask
from flask_restful import Api, Resource, request
from flask_cors import CORS
import threading
from header import s

import grpc
import registry.stocks_pb2_grpc
import registry.stocks_pb2

from transactions_history_recorder import add_transaction
from python_mongo_client import add_customer
from message_producer import sendMessage

channel = grpc.insecure_channel('localhost:8501')
stub = registry.stocks_pb2_grpc.RegisteringTransactionStub(channel)

app = Flask(__name__)
CORS(app)
api = Api(app)

class BuyOrder(Resource):

    def buyOrder(self, dbid, symbol, price, qty):
        status = "rejected"
        new_price = 0
        price = float(price)
        while True:
            data = s.get(f"https://www.nseindia.com/api/quote-equity?symbol={symbol}")
#            if(data.json()['metadata']['lastUpdateTime'].find("16:00:00") != -1):
#               print(data.json()['metadata']['lastUpdateTime'].find("16:00:00"))
#                add_transaction(dbid, symbol, qty, price, "failed")
#                sendMessage(dbid, f"Your order for {symbol}, {price}, {qty} has been rejected due to market is closed")
#                break
#            el
            if(float(data.json()['priceInfo']['lastPrice']) <= price):
                new_price = float(data.json()['priceInfo']['lastPrice'])
                status = "success"
                break
            pass
        print(status)
        if(status == "success"):
            fund = stub.GetFund(registry.stocks_pb2.DbID(dbid=dbid))
            if(fund.fund < (new_price * int(qty))):
                add_transaction(dbid, symbol, qty, price, "failed")
                sendMessage(dbid, f"Your order for {symbol}, {price}, {qty} has been rejected due to insufficient funds")
                return
            else:
                add_transaction(dbid, symbol, qty, new_price, "success")
                stub.Buy(registry.stocks_pb2.NotingTransaction(dbid=dbid, symbol=symbol, qty=int(qty), price=float(new_price)))
                sendMessage(dbid, f"Your order for {symbol}, {price}, {qty} has been executed")
                return
        else:
            add_transaction(dbid, symbol, qty, price, "failed")
            sendMessage(dbid, f"Your order for {symbol}, {price}, {qty} has been rejected due to market is closed")
        return

    def post(self):
        dbid = request.json['dbid']
        symbol = request.json['symbol']
        price = request.json['price']
        qty = request.json['qty']
        buyThread = threading.Thread(target=self.buyOrder, args=(dbid, symbol, price, qty))
        buyThread.start()
        return {"msg": "Order Placed here"}
    pass

class SellOrder(Resource):
    
    def sellOrder(self, dbid, symbol, price, qty):
        status = "rejected"
        new_price = 0
        price = float(price)
        while True:
            data = s.get(f"https://www.nseindia.com/api/quote-equity?symbol={symbol}")
#            if(data.json()['metadata']['lastUpdateTime'].find("16:00:00") != -1):
#                break
#            el
            if(float(data.json()['priceInfo']['lastPrice']) >= price):
                new_price = float(data.json()['priceInfo']['lastPrice'])
                status = "success"
                break
            pass
        if(status == "success"):
            shares = stub.GetShareQty(registry.stocks_pb2.ShareQuery(dbid=dbid, symbol=symbol))
            if(shares.qty < int(qty)):
                add_transaction(dbid, symbol, qty, -price, "failed")
                sendMessage(dbid, f"Your sell order for {symbol}, {price}, {qty} has been rejected due to insufficient shares")
                return
            else:
                add_transaction(dbid, symbol, qty, -new_price, "success")
                stub.Sell(registry.stocks_pb2.NotingTransaction(dbid=dbid, symbol=symbol, qty=int(qty), price=float(new_price)))
                sendMessage(dbid, f"Your sell order for {symbol}, {price}, {qty} has been executed")
                return
        else:
            add_transaction(dbid, symbol, qty, -price, "failed")
            sendMessage(dbid, f"Your  sell order for {symbol}, {price}, {qty} has been reected due to market is closed")
        return

    def post(self):
        dbid = request.json['dbid']
        symbol = request.json['symbol']
        price = request.json['price']
        qty = request.json['qty']
        sellThread = threading.Thread(target=self.sellOrder, args=(dbid, symbol, price, qty))
        sellThread.start()
        return {"msg": "Order Placed"}
    pass

class AddCustomer(Resource):
    def post(self):
        dbid = request.json['dbid']
        add_customer(dbid)
        return {"msg": "Customer Added"}
    def get(self):
        return {"msg": "Customer Added"}
    pass

api.add_resource(BuyOrder, '/api/buy')
api.add_resource(SellOrder, '/api/sell')
api.add_resource(AddCustomer, '/api/add')
app.run(debug=True, port=8301)
