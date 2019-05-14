from socket  import *
import threading
import sys

def receive(socket, signal):
    while signal:
        try:
            data = socket.recv(1024)
            print(str(data.decode("utf-8")))
        except:
            print("You have been disconnected from the server")
            signal = False
            break


def byt(text):
	return bytes(text, "utf-8")


s = socket(AF_INET, SOCK_STREAM)
s.connect(("127.0.0.1", 10545)) # connect to server (block until accepted)
#s.send(bytes('Hello, world', "utf-8"))  # send some data

receiveThread = threading.Thread(target = receive, args = (s, True))
receiveThread.start()

#Send data to server
#str.encode is used to turn the string message into bytes so it can be sent across the network
while True:
    message = input()
    s.sendall(str.encode(message))






#sent = input()
#s.send(byt(sent))
#data = s.recv(1024).decode()     # receive the response


#print(data)              # print the result
s.close()               # close the connection
