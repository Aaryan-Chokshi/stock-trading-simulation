import grpc
import registry.stocks_pb2_grpc
import registry.stocks_pb2
import concurrent.futures as futures
from python_mongo_client import get_fund, get_shares, sell_share, buy_share

class RegisteringTransaction(registry.stocks_pb2_grpc.RegisteringTransactionServicer):
    def GetFund(self, request, context):
        funds = get_fund(request.dbid)
        return registry.stocks_pb2.FundResponse(fund=funds)
    def GetShareQty(self, request, context):
        print(request.dbid, request.symbol)
        qty = get_shares(request.dbid, request.symbol)
        return registry.stocks_pb2.ShareQtyResponse(qty=qty)
    def Buy(self, request, context):
        buy_share(request.dbid, request.symbol, request.qty, request.price)
        return registry.stocks_pb2.Message(message="Success")
    def Sell(self, request, context):
        sell_share(request.dbid, request.symbol, request.qty, request.price)
        return registry.stocks_pb2.Message(message="Success")
    pass

server = grpc.server(futures.ThreadPoolExecutor(max_workers=100))
registry.stocks_pb2_grpc.add_RegisteringTransactionServicer_to_server(
        RegisteringTransaction(), server)


server.add_insecure_port('[::]:8501')
server.start()
server.wait_for_termination()
