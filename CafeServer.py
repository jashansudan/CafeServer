import socket
import threading
import collections
import json

# Main thread for handling client connections
class ClientThread(threading.Thread):
    def __init__(self, caddress, csocket):
        threading.Thread.__init__(self)
        self.client_socket = csocket
        self.client_address = caddress
        self.urls = 0
        # Fulfills requirement 2
        self.access_code = 0
        self.client_name = "client" + str(client_stats.sessions)
        print ("New connection added: ", self.client_address)

    # Run method for the thread
    def run(self):
        # This is to record the number of connected clients
        connection.increment_conn()
        connect = True

        # Disconnect the client if the number of concurrent connections > 3
        # Fulfills requirement 7
        if connection.get() > 3:
            self.client_socket.send(bytes("Close"))
            connect = False
        print "Number of currently connected clients: " + str(connection.get())

        # If client connected, increment the client number for next user
        if connect:
            print "Client name is: " + self.client_name
            client_stats.inc_sessions()

        # While the client is connected handle requests
        while connect:
            data = self.client_socket.recv(2048)
            msg = data.decode()
            print "Message from client: " + msg

            # Set up acess code and urls for client
            if self.access_code == 0:
                self.setup_user_access(msg)
                self.client_socket.send(bytes("You are now connected to the server!"))
            # If platinum and requests stats return client usage
            # Fulfills requirement 8
            elif msg == "http://clientsusage.com":
                if self.access_code % 10 != 0:
                    self.client_socket.send(bytes("You do not have access!"))
                else:
                    self.client_socket.send(bytes(client_stats.get_stats()))
            # If client wants to manuall disconnect, free resources
            elif msg == 'exit':
                break
            # Return a response to client request
            else:
                # Fulfills requirement 3
                fullfilled = "Request not fulfilled"
                if responses.random_response(msg) != "No response available for request!":
                    fullfilled = "Request fullfilled"
                # Fulfills requirement 10
                client_stats.log_details(self.client_name, (str(msg), fullfilled))
                self.client_socket.send(bytes(responses.random_response(msg)))
                self.urls -= 1
                # fulfills requirement 5
                if self.urls == 0 or self.urls == -11:
                    # Fulfills requirement 7
                    self.client_socket.send(bytes("Close"))
                    break

        # Free resources and track usage
        connection.decrement_conn()
        print "There are now " + str(connection.get()) + " concurrent connections!"
        print ("Client at ", self.client_address, " disconnected...")

    # Assign a user access code
    def setup_user_access(self, msg):
        self.access_code = int(msg)
        if self.access_code % 10 == 0:
            self.urls = -1
        elif self.access_code % 2 == 0:
            self.urls = 3
        else:
            self.urls = 5


# Class for mapping responses to requests
class Responses:
    def __init__(self):
        self.response_map = {"google.com": "g", "microsoft.com": "m",
                             "github.com": "g"}

    def random_response(self, key):
        if key in self.response_map:
            return self.response_map[key]
        else:
            return "No response available for request!"

# Class for tracking concurrent connections
class Connection:
    def __init__(self):
        self.connections = 0

    def get(self):
        return self.connections

    def increment_conn(self):
        self.connections += 1

    def decrement_conn(self):
        self.connections -= 1


# Class for logging client requests and sessions
class ClientStats:
    # Class tracks total number of clients connected and logs their info
    def __init__(self):
        self.sessions = 1
        self.usage_map = collections.defaultdict(list)

    def inc_sessions(self):
        self.sessions += 1

    def dec_sessions(self):
        self.sessions -= 1

    # Used to log client information
    def log_details(self, key, val):
        self.usage_map[key].append(val)

    def get_stats(self):
        return json.dumps(self.usage_map)

# Class for the server, does inital setup
class Server:
    def __init__(self):
        # Setting up server
        # Fulfills requirement 1
        LOCALHOST = "127.0.0.1"
        PORT = 8080
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((LOCALHOST, PORT))
        print("Server started")
        print("Waiting for client request..")
        while True:
            # Server listens for new requests and creats a thread for each one
            # Fulfills requirement 4
            server.listen(1)
            clientsock, clientAddress = server.accept()
            newthread = ClientThread(clientAddress, clientsock)
            newthread.start()


# Logging classess used by the server
responses = Responses()
connection = Connection()
client_stats = ClientStats()
