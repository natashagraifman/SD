from socket  import *
from threading import Thread

def convByte(texto):
	#transforma string em bytes
	return bytes(texto, "utf-8")

def recebeServer(socket, sinal):
	#recebe mensagem do servidor e printa pro usuário
	while sinal:
		try:
			msgServer = socket.recv(4096)
			print(str(msgServer.decode("utf-8")))
		except:
			print("Você foi desconectado.")
			break

def enviaServer(socket, sinal):
	#envia input do usuário pro servidor
	while sinal:
		try:
			sent = input()
			s.send(convByte(sent))
		except:
			print("Você foi desconectado.")
			break

host = "127.0.0.1"
port = 33000

s = socket(AF_INET, SOCK_STREAM)
s.connect((host, port))

Thread(target = recebeServer, args = (s, True)).start()
Thread(target = enviaServer, args = (s, True)).start()