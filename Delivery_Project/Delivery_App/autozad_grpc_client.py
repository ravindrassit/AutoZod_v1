
import grpc
from . import autozad_pb2
from . import autozad_pb2_grpc

def get_example_data(request_data):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = autozad_pb2_grpc.AutoZad_ServiceStub(channel)
        request = autozad_pb2.ItemRequest(request_data=request_data)
        response = stub.GetItem(request)
        return response.response_data