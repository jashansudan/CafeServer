# A TCP client server model in python for CISC 435: Computer Networks

## Requirements for this project:

* Client's have a random access code they connect to the server with
* Depending on the access code, they are allowed a certain number of requests
* Clients can make request to the server and return dummy responses
* A Client that hits it's quota for requests will be disconnected
* Client's whose random access code ends with 0, can view all client's server usage
* Server can handle up to 3 clients