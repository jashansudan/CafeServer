import socket
from random import *
import json
import time


# Class for standard client
class Client:
    def __init__(self, a_code):
        # Set up basic client information, like access code
        SERVER = "127.0.0.1"
        PORT = 8080
        if a_code == 0:
            access_code = randint(50, 300)
        else:
            access_code = a_code
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER, PORT))
        client.sendall(bytes(access_code))
        out_data = ""

        # Continuously communicate with server, sending messages
        while True:
            in_data = (client.recv(2048)).decode()
            # End connection and deallocate resources
            if in_data == "Close":
                print "Quota has been hit and connection is closed."
                break
            # Last request was stats, so parse them
            elif out_data == "http://clientsusage.com" and in_data != "You do not have access!":
                print ""
                usage = json.loads(in_data)
                for i in usage:
                    usage[i] = [str(j) for j in usage[i]]
                for i in usage:
                    print i, usage[i]
                    print ""
            # Send standard request
            else:
                print("From Server :", in_data)
            out_data = raw_input()
            client.sendall(out_data)
            if out_data == 'exit':
                print "Client has chosen to disconnect early!"
                break
        client.close()

# Sample client to emulate a user sending requets
class ClientWithReqAndResponses:
    def __init__(self, a_code):
        # Set up basic client information, like access code
        SERVER = "127.0.0.1"
        PORT = 8080
        if a_code == 0:
            access_code = randint(50, 300)
        else:
            access_code = a_code
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER, PORT))
        client.sendall(bytes(access_code))
        out_data = ""
        count = 0
        # Continuously communicate with server, sending messages
        while True:
            count += 1
            in_data = (client.recv(2048)).decode()
            # End connection and deallocate resources
            if in_data == "Close":
                print "Quota has been hit and connection is closed."
                break
            # Last request was stats, so parse them
            elif out_data == "http://clientsusage.com" and in_data != "You do not have access!":
                print ""
                usage = json.loads(in_data)
                for i in usage:
                    usage[i] = [str(j) for j in usage[i]]
                for i in usage:
                    print i, usage[i]
                    print ""
            # Send standard request
            else:
                # Fulfills requirement 9
                print("From Server :", in_data)
            out_data = "google.com"
            if access_code % 10 == 0 and count == 9 or access_code == 3 and count == 4:
                out_data = "http://clientsusage.com"
            client.sendall(out_data)
            if out_data == 'exit':
                print "Client has chosen to disconnect early!"
                break
        client.close()

# Timed client that disconnects after a short period of time
class Timed_Client:
    def __init__(self):
        # Set up basic client information, like access code
        SERVER = "127.0.0.1"
        PORT = 8080
        access_code = randint(50, 300)
        print "Client access code is: ", access_code
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER, PORT))
        client.sendall(bytes(access_code))
        out_data = ""

        # Continuously communicate with server, sending messages
        while True:
            in_data = (client.recv(2048)).decode()
            print("From Server :", in_data)
            # End connection and deallocate resources
            time.sleep(10)
            out_data = 'exit'
            client.sendall(out_data)
            if out_data == 'exit':
                print "Client has chosen to disconnect early!"
                break
        client.close()
