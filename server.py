from socket  import *
from threading import Thread
import os

connections = []
total_connections = 0


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

		if(autor == usuario + "\n"):
			arq.close()
			os.remove(diretorio + titulo + ".txt")

			return "Publicação apagada."
		else:
			return "Você não tem permissões para apagar essa publicação."
	else:
		return "Publicação não encontrada."

def pegaNomes():
	#Pega o nome de todos os autores que publicaram pelo menos uma vez
	nomes = ""
	
	for root,dirs,files in os.walk(diretorio):
		for publicacao in files:
			arq = open(diretorio + publicacao, "r")
			autor = arq.readline()
			if autor not in nomes:
				nomes += autor + "\n"
	return nomes

def convByte(texto):
	return bytes(texto, "utf-8")

def recebeConexoesThread(socket):
	while True:
		s, address = socket.accept()
		Thread(target=opcoesUsuarioThread, args=(s, adress)).start()

def opcoesUsuarioThread(client, ip):

	client.send(convByte("Escreva seu nome:"))
	usuario = client.recv(4096).decode()

	client.send(convByte("\nEscreva o número da opção desejada:\n\n1 - Ver todas as publicações\n2 - Escrever uma nova publicação\n3 - Ler publicação\n4 - Apagar publicação\n5 - Se inscrever\n6 - Sair\n"))

	if(True):
		while(True):
			opcao = client.recv(4096).decode()
			
			if(opcao == "1"):
				client.send(convByte(mostraPublicacoes()))

			elif(opcao == "2"):
				client.send(convByte("Escreva o título da sua publicação:\n"))
				titulo = client.recv(4096).decode()
				client.send(convByte("Escreva o conteúdo:\n"))
				texto = client.recv(4096).decode()
				if(novaPublicacao(titulo, usuario, texto)):
					client.send(convByte("Publicação salva!\n"))
				else:
					client.send(convByte("Erro ao concluir publicação.\n"))
				continue

			elif(opcao == "3"):
				client.send(convByte("Escreva o título da publicação que deseja ler:\n"))
				titulo = client.recv(4096).decode()
				client.send(convByte(lerPublicacao(titulo)))
				continue

			elif(opcao == "4"):
				client.send(convByte("Escreva o título da publicação que quer apagar:\n Obs.:Você só pode apagar uma publicação de sua autoria!\n"))
				titulo = client.recv(4096).decode()
				client.send(convByte(deletaPublicacao(titulo, usuario)))
				continue

			elif(opcao == "5"):
				#Printa o nome de todos os autores disponíveis para inscrição
				client.send(convByte("Nome dos autores que você pode se inscrever:")) 
				client.send(convByte(pegaNomes))
				client.send(convByte("Em qual deseja se inscrever?"))
				autor = client.recv(4096).decode()
				client.send(convByte(salvaInscricao(autor, usuario)))
				continue

			elif(opcao == "6"):
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
recebeConexoesThread(s)
