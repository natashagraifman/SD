from socket  import *
from threading import Thread
import os

def mostraPublicacoes():
	global diretorio

	todasPub = ""

	for root,dirs,files in os.walk(diretorio):
		for publicacao in files:
			publicacao = (publicacao.split(".")[0])
			todasPub += publicacao + "\n"

	if(todasPub == ""):
		return "Nenhuma publicação."
		
	else:
		return todasPub

def novaPublicacao(titulo, usuario, texto):
	global diretorio

	try:
		arq = open(diretorio + titulo + ".txt", "w")
		arq.write(usuario + "\n" + texto)
		arq.close()
		return True

	except:
		print("Erro ao criar nova publicação.")
		return False

def lerPublicacao(titulo):
	global diretorio

	if(os.path.isfile(diretorio + titulo + ".txt")):
		arq = open(diretorio + titulo + ".txt", "r")
		texto = arq.read()
		arq.close()
		return texto

	else:
		return "Publicação não existe."

def deletaPublicacao(titulo, usuario):
	global diretorio

	if(os.path.isfile(diretorio + titulo + ".txt")):
		arq = open(diretorio + titulo + ".txt", "r")
		autor = arq.readline()

		if(autor == usuario):
			os.remove(diretorio + titulo + ".txt")
			return True
		
		arq.close()

	else:
		return False

def convByte(texto):
	return bytes(texto, "utf-8")

def recebeConexoesThread():
	
	global exit

	while(not exit):
		client, ip = s.accept()
		print(str(ip) + " has connected.")
		client.send(convByte("Connected\n"))
		Thread(target=opcoesUsuarioThread, args=(client, ip)).start()

def opcoesUsuarioThread(client, ip):

	client.send(convByte("Digite seu nome:"))
	usuario = client.recv(4096).decode()

	client.send(convByte("\nDigite o número da opção desejada:\n\n1 - Ver todas as publicações\n2 - Escrever uma nova publicação <titulo em 1 palavra> <texto>\n3 - Ler <publicacao>\n4 - Apagar <publicacao>\n5 - Sair\n"))

	if(True):
		while(True):
			entrada = client.recv(4096).decode()
			opcao = entrada.split(" ")[0]
		
			if(opcao == "1"):
				client.send(convByte(mostraPublicacoes()))
			
			elif(opcao == "2"):
				titulo = entrada.split(" ")[1]
				texto = " ".join(entrada.split(" ")[2:])
				if(novaPublicacao(titulo, usuario, texto)):
					client.send(convByte("Message successfully sent\n"))
				else:
					client.send(convByte("There was a problem in your message\n"))
				continue

			elif(opcao == "3"):
				publicacao = entrada.split(" ")[1]
				client.send(convByte(lerPublicacao(publicacao)))
				continue

			elif(opcao == "4"):
				publicacao = entrada.split(" ")[1]
				if(deletaPublicacao(publicacao, usuario)):
					client.send(convByte("Publicação apagada\n"))
				else:
					client.send(convByte("Publicação não encontrada\n"))
				continue

			elif(opcao == "5"):
				client.send(convByte("exit"))
				print(str(ip) + " disconnected\n")
				return

diretorio = os.getcwd() + "\\Publicações\\"

host = "127.0.0.1"
port = 33000
adress = (host, port)
exit = False

if(not os.path.exists(diretorio)):
	os.system("mkdir Publicações")

s = socket(AF_INET, SOCK_STREAM) 
s.bind((host, port))  
s.listen(1)           
recebeConexoesThread()