# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import stocks_pb2 as stocks__pb2


class RegisteringTransactionStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetFund = channel.unary_unary(
                '/RegisteringTransaction/GetFund',
                request_serializer=stocks__pb2.DbID.SerializeToString,
                response_deserializer=stocks__pb2.FundResponse.FromString,
                )
        self.GetShareQty = channel.unary_unary(
                '/RegisteringTransaction/GetShareQty',
                request_serializer=stocks__pb2.ShareQuery.SerializeToString,
                response_deserializer=stocks__pb2.ShareQtyResponse.FromString,
                )
        self.Buy = channel.unary_unary(
                '/RegisteringTransaction/Buy',
                request_serializer=stocks__pb2.NotingTransaction.SerializeToString,
                response_deserializer=stocks__pb2.Message.FromString,
                )
        self.Sell = channel.unary_unary(
                '/RegisteringTransaction/Sell',
                request_serializer=stocks__pb2.NotingTransaction.SerializeToString,
                response_deserializer=stocks__pb2.Message.FromString,
                )


class RegisteringTransactionServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetFund(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetShareQty(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Buy(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Sell(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RegisteringTransactionServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetFund': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFund,
                    request_deserializer=stocks__pb2.DbID.FromString,
                    response_serializer=stocks__pb2.FundResponse.SerializeToString,
            ),
            'GetShareQty': grpc.unary_unary_rpc_method_handler(
                    servicer.GetShareQty,
                    request_deserializer=stocks__pb2.ShareQuery.FromString,
                    response_serializer=stocks__pb2.ShareQtyResponse.SerializeToString,
            ),
            'Buy': grpc.unary_unary_rpc_method_handler(
                    servicer.Buy,
                    request_deserializer=stocks__pb2.NotingTransaction.FromString,
                    response_serializer=stocks__pb2.Message.SerializeToString,
            ),
            'Sell': grpc.unary_unary_rpc_method_handler(
                    servicer.Sell,
                    request_deserializer=stocks__pb2.NotingTransaction.FromString,
                    response_serializer=stocks__pb2.Message.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'RegisteringTransaction', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RegisteringTransaction(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetFund(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RegisteringTransaction/GetFund',
            stocks__pb2.DbID.SerializeToString,
            stocks__pb2.FundResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetShareQty(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RegisteringTransaction/GetShareQty',
            stocks__pb2.ShareQuery.SerializeToString,
            stocks__pb2.ShareQtyResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Buy(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RegisteringTransaction/Buy',
            stocks__pb2.NotingTransaction.SerializeToString,
            stocks__pb2.Message.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Sell(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RegisteringTransaction/Sell',
            stocks__pb2.NotingTransaction.SerializeToString,
            stocks__pb2.Message.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
