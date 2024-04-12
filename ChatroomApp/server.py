import threading
import socket
import argparse
import os

class Server(threding.Thread):

    def __init__(self, host, port):
        super().__init__()
        self.connecttion = []
        self.host = host 
        self.port = port 
    
    def run(self):
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))

        sock.listen(1)
        print("Listening at", sock.getsockname())

        while True:

            # Accepting new connection
            sc, sockname = sock.accept()
            print(f"Accepting a new connection from {sc.getpeername()} to {sc.getsockname()}")

            # Create a new thread
            server_socket = ServerSocket(sc, sockname, self)

            # start new thread
            server_socket.start()

            # Add thread to active connection
            self.connections.append(server_socket)
            print("Ready to recieve message from", sc.getpeername())

    
    def broadcast(self, message, source):
        for connection in self.connection:

            # send to all connected client accept the source client
            if connection.sockname != source:
                connection.send(message)

    def remove_connection(self, connection):

        self.connections.remove(connection)
