from socket  import *
from threading import Thread

def convByte(texto):
	return bytes(texto, "utf-8")

def recebeServer(socket, sinal):
	while sinal:
		try:
			msgServer = socket.recv(4096)
			print(str(msgServer.decode("utf-8")))
		except:
			print("Você foi desconectado.")
			sinal = False
			break

def enviaServer(socket, sinal):
	while sinal:
		try:
			sent = input()
			s.send(convByte(sent))
		except:
			print("Você foi desconectado.")
			sinal = False
			break

host = "127.0.0.1"
port = 33000

s = socket(AF_INET, SOCK_STREAM)
s.connect((host, port))

Thread(target = recebeServer, args = (s, True)).start()
Thread(target = enviaServer, args = (s, True)).start()