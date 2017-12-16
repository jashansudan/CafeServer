import CafeServer
import client
import threading
import time


# This creates the server used for all tests
def create_server():
    print "Creating Server"
    server = threading.Thread(name='server', target=CafeServer.Server)
    server.start()
    time.sleep(1)


# This test checks to see if multiple clients can be connected, max 3
def test_multiple_clients():
    print "\nConnecting Client 1"
    client1 = threading.Thread(name='client', target=client.Timed_Client)
    client1.start()
    time.sleep(1)

    print "\nConnecting Client 2"
    client2 = threading.Thread(name='client', target=client.Timed_Client)
    client2.start()
    time.sleep(1)

    print "\nConnecting Client 3"
    client3 = threading.Thread(name='client', target=client.Timed_Client)
    client3.start()
    time.sleep(1)

    print "\nConnecting Client 4"
    client4 = threading.Thread(name='client', target=client.Timed_Client)
    client4.start()

    time.sleep(11)

    print "\nConnecting Client 4"
    client5 = threading.Thread(name='client', target=client.Timed_Client)
    client5.start()


# This test confirms that a random access code is assigned
def test_random_access_code():
    print "\nConnecting random access code client"
    random_code = threading.Thread(name='client', target=client.Timed_Client)
    random_code.start()


# This test confirms that clients ending in a 2, except 0, have a 3 url limit
def test_3_rate_limit():
    print "\nConnecting 3 url limit client"
    rate_limit_client = threading.Thread(name='client', target=client.ClientWithReqAndResponses, args=[2])
    rate_limit_client.start()


# This test confirms that clients ending in a odd number, have a 5 url limit
def test_5_rate_limit():
    print "\nConnecting 5 url limit client"
    rate_limit_client = threading.Thread(name='client', target=client.ClientWithReqAndResponses, args=[3])
    rate_limit_client.start()


# This test confirms that clients ending in 0, have unlimited urls and can check stats
# This test has a timeout after 11 requests, to ensure it doesn't forever loop, the main client code does not have this
def test_unlimited_rate_and_stats():
    print "\nConnecting unlimited url limit client"
    unlimited_client = threading.Thread(name='client', target=client.ClientWithReqAndResponses, args=[10])
    unlimited_client.start()


create_server()
print "\nTesting multiple concurrent client connections!"
test_multiple_clients()
time.sleep(11)
print "\nTesting if a random access code is assigned!"
test_random_access_code()
time.sleep(11)
time.sleep(11)
print "\nTesting clients with access code ending in a even number have a 3 url limit!"
test_3_rate_limit()
time.sleep(5)
print "\nTesting clients with access code ending in a odd number have a 5 url limit!"
test_5_rate_limit()
time.sleep(5)
print "\nTesting clients with access code ending in a 0 have unlimited urls!"
test_unlimited_rate_and_stats()
