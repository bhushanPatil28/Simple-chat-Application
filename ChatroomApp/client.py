import threading
import socket
import argparse
import os
import sys
import tkinter as tk 


class Send(threading.Thread):

    # Listens for user input from command line

    # sock the connected sock object
    # name (str) : The user

    def __init__(self, sock, name):

        super().__init__()
        self.sock = sock 
        self.name = name 

    def run(self):
        '''Listen for user input from the command line and send
           send it to the server
           Typing "Quit" will close the connection and exit the 
           app'''
        while True:
            print('{}: '.format(self.name), end='')
            sys.stdout.flush()
            message = sys.stdin.readline()[:-1]

            # if we type "QUIT" we will leave the chatroom
            
            if message == "QUIT":
                self.sock.sendall('Server: {} has left the chat.'.format(self.name).encode('ascii'))
                break 

            # send message ot server for broadcasting

            else:
                self.sock.sendall('{}: {} .'.format(self.name, message).encode('ascii'))
            
        print('\nQuitting...')
        self.sock.close()
        os.exit(0)


class Receive(threading.Thread):

    # Listnes for the incoming messages fromt the server
    def __init__(self, sock, name):

        super().__init__()
        self.sock = sock
        self.name = name
        self.messages = None

    def run(self):

        # Receives data from the server and displays it in the gui

        while True:
            message = self.sock.recv(1024).decode('ascii')

            if message:

                if self.messages:
                    self.messages.insert(tk.END, message)
                    print('\r{}\n{}: '.format(message, self.name),end='')
                
                else:
                    print('\r{}\n{}: '.format(message, self.name),end='')
            
            else:
                print('\n we have lost the connection to the server')
                print('\nQuitting...')
                self.sock.close()
                os.exit(0)

class Client:

    # Will manage client-server connection and integration of GUI

     def __init__(self, host, port):

        self.host = host
        self.port = port 
        self.sock = socket.socket(socket.Af_INET, socket.SOCK_STREAM)
        self.name = None 
        self.messages = None

     def start(self):
         print('Trying to connect to {}:{}...', format(self.host, self.port))

         self.sock.connect((self.host, self.port))

         print("Successfully connected to {}:{}".format(self.host, self.port))


         print()

         self.name = input('Your name: ')
         
         print()

         print('Welcome, {}! Getting ready to send and recieve messages'.format(self.name))

        #  Create send and recieve threads

         send = Send(self.sock, self.name)

         receive = Receive(self.sock, self.name)

        #  start send and recieve thread
         send.start()
         receive.start()

         self.sock.sendall('server: {} has joined the chat. say whatsup!'.format(self.name).encode('ascii'))
         print("\rReady! Leave the chatroom anytime by typing 'QUIT'\n")
         print('{}: '.format(self.name), end='')

         return receive
     
     def exit(self, textInput):