from flask import Flask
from flask_restful import Api, Resource, request
from flask_cors import CORS

from python_mongo_client import get_shares_list, get_fund
from transactions_history_recorder import read_transactions


app = Flask(__name__)
CORS(app)
api = Api(app)

class HoldingDetails(Resource):
    def get(self, dbid):
        return {"shares": get_shares_list(dbid), "fund": get_fund(dbid)}
    pass

class TransactionsHistory(Resource):      
    def get(self, dbid):
        return {"data": read_transactions(dbid)}
    pass

api.add_resource(HoldingDetails, '/api/holding_details/<string:dbid>')
api.add_resource(TransactionsHistory, '/api/transactions_history/<string:dbid>')

app.run(debug=True, port=8401)