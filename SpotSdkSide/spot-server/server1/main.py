

from concurrent import futures
import grpc
from robot_id_service_pb2_grpc import *
import robot_id_service_pb2_grpc


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    robot_id_service_pb2_grpc.add_RobotIdServiceServicer_to_server(
        RobotIdServiceServicer(), server)
    server.add_insecure_port('[::]:443')
    server.start()
    server.wait_for_termination()
    
if __name__ == "__main__":
    serve()