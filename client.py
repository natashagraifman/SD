from socket  import *

def byt(text):
	return bytes(text, "utf-8")
s = socket(AF_INET, SOCK_STREAM)
s.connect(("127.0.0.1", 10545)) # connect to server (block until accepted)
#s.send(bytes('Hello, world', "utf-8"))  # send some data
sent = input()
s.send(byt(sent))
data = s.recv(1024).decode()     # receive the response


print(data)              # print the result
s.close()               # close the connection
