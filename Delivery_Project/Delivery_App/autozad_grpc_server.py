# service_pb2_grpc.py and service_pb2.py are generated files

'''import grpc
from concurrent import futures
import autozad_pb2
# import service_pb2_grpc
import autozad_pb2_grpc
import requests

class MyService(autozad_pb2_grpc.autozad_serviceServicer):
    def GetItem(self, request, context):
        # return autozad_pb2.HelloReply(message='Hello, %s!' % request.name)

        # Extract the order ID from the request (if required)
        # order_id = request.order_id

        # Mock order_id for demonstration; in practice, use request.order_id
        # order_id = '12345'

        # Make a request to your Django API
        api_url = f'http://localhost:8080/api/delivery/'
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            api_data = response.json()

            # Construct the OrderReply message using the data from Django API
            return autozad_pb2.ItemResponse(
                order_id=api_data.get('order_id', ''),
                merchant_name=api_data.get('merchant_name', ''),
                deliver_name=api_data.get('deliver_name', ''),
                partnerId=api_data.get('partnerId', '')
            )
        except requests.RequestException as e:
            # Handle errors, for example by returning an error message
            print(f"Error fetching data from Django API: {e}")
            # Return default or error message; adjust as needed
            return autozad_pb2.ItemResponse(
                order_id='',
                merchant_name='',
                deliver_name='',
                partnerId=''
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    autozad_pb2_grpc.add_autozad_serviceServicer_to_server(MyService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
'''