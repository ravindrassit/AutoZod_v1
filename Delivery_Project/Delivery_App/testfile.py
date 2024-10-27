# test_grpc_import.py
try:
    import grpc
    print("grpc module is available.")
except ModuleNotFoundError as e:
    print(f"Module not found: {e}")

try:
    from grpc_tools import protoc
    print("grpc_tools module is available.")
except ModuleNotFoundError as e:
    print(f"Module not found: {e}")
