from socket  import *
import threading

def convByte(texto):
	return bytes(texto, "utf-8")

def receive(socket, signal):
	while signal:
		try:
			data = socket.recv(1024)
			print(str(data.decode("utf-8")))
		except:
			print("You have been disconnected from the server")
			signal = False
			break

def send(socket, signal):
	while signal:
		try:
			sent = input()
			s.send(convByte(sent))
		except:
			print("You have been disconnected from the server")
			signal = False
			break

host = "127.0.0.1" #MUDAR O IP SE NECESSÁRIO
port = 33000

s = socket(AF_INET, SOCK_STREAM)
s.connect((host, port))

#msgServer = s.recv(1024).decode()
#print(msgServer)

sendThread = threading.Thread(target = send, args = (s, True))
sendThread.start()
receiveThread = threading.Thread(target = receive, args = (s, True))
receiveThread.start()
