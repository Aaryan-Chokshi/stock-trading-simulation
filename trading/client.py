import grpc
import registry.stocks_pb2_grpc
import registry.stocks_pb2

channel = grpc.insecure_channel('localhost:8501')
stub = registry.stocks_pb2_grpc.RegisteringTransactionStub(channel)

request = registry.stocks_pb2.DbID(dbid='1')

response = stub.GetFund(request)
