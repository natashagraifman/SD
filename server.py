from socket  import *
from threading import Thread
import os

def mostraPublicacoes():
	#Printa na tela o título de todas as publicações
	
	todasPub = ""

	for root,dirs,files in os.walk(publish):
		for publicacao in files:
			publicacao = (publicacao.split(".")[0])
			todasPub += publicacao + "\n"

	if(todasPub == ""):
		return "Nenhuma publicação."

	else:
		return todasPub

def novaPublicacao(titulo, usuario, texto):
	#cria um novo arquivo na pasta publicações com o titulo da publicação sendo o nome do arquivo, e escreve o nome do autor e o conteúdo
	try:
		arq = open(publish + titulo + ".txt", "w")
		arq.write(usuario + "\n" + texto)
		arq.close()
		atualizaFlags(usuario)
		return True

	except:
		print("Erro ao criar nova publicação.")
		return False

def lerPublicacao(titulo):
	#Procura publicação digitada e se existir, printa ela na tela

	if(os.path.isfile(publish + titulo + ".txt")):
		arq = open(publish + titulo + ".txt", "r")
		texto = arq.read()
		arq.close()
		return texto

	else:
		return "Publicação não existe."

def deletaPublicacao(titulo, usuario):
	#se a pessoa que tenta apagar é a autora do arquivo e ele existe, ele é apagado

	if(os.path.isfile(publish + titulo + ".txt")):
		arq = open(publish + titulo + ".txt", "r")
		autor = arq.readline()

		if(autor == usuario + "\n"):
			arq.close()
			os.remove(publish + titulo + ".txt")

			return "Publicação apagada."
		else:
			return "Você não tem permissões para apagar essa publicação."
	else:
		return "Publicação não encontrada."

def pegaNomes():
	#Pega o nome de todos os autores que publicaram pelo menos uma vez
	nomes = ""
	
	for root,dirs,files in os.walk(publish):
		for publicacao in files:
			arq = open(publish + publicacao, "r")
			autor = arq.readline()
			if autor not in nomes:
				nomes += autor
		arq.close()
	return nomes

def salvaInscricao(autor, usuario):
	#Salva num arquivo o autor e seus inscritos, desde que o autor não seja o proprio usuário
	arq = open(subscribe + autor + ".txt", "r")
	inscritos = arq.read()
	arq.close()
	if (usuario == autor):
		return "Você não pode se inscrever em si mesmo."
	elif (usuario in inscritos):
		return "Você já está inscrito nesse autor."
	else:		
		arq = open(subscribe + autor + ".txt", "a")	
		arq.write(usuario + " 0" + "\n")
		arq.close()
		return "Inscrição realizada com sucesso!"

def atualizaFlags(usuario):
	#Nos arquivos de inscrição, muda pra 1 as flags de todos os inscritos desse autor
	if(os.path.isfile(subscribe + usuario + ".txt")):
		arq = open(subscribe + usuario + ".txt", "r")
		inscritos = arq.read()
		arq.close()
		inscritos = inscritos.replace("0", "1")		
		arq = open(subscribe + usuario + ".txt", "w")
		arq.write(inscritos)
		arq.close()

def geraNotificacao(usuario, autor):
	#Se usuário estiver com flag 1 em algum arquivo, muda a flag pra 0 e manda notificação daquele autor
	arq = open(subscribe + autor, "r")
	inscritos = arq.read()
	arq.close()
	if (usuario in inscritos):
		inscritos = inscritos.replace(usuario + " 1", usuario + " 0")
		arq = open(subscribe + autor, "w")
		arq.write(inscritos)
		arq.close()
		autor = (autor.split(".")[0])
		#manda mensagem de notificação
		return "Você tem uma nova publicação de " + autor + "\n"

def convByte(texto):
	#transforma string em bytes
	return bytes(texto, "utf-8")

def recebeConexoesThread(socket):
	#Aceita todas as requisições de conexão e inicia uma thread pra cada usuário
	while True:
		s, address = socket.accept()
		Thread(target=opcoesUsuarioThread, args=(s, adress)).start()

def opcoesUsuarioThread(client, ip):
	#menu de opções pro usuário
	client.send(convByte("Escreva seu nome:"))
	usuario = client.recv(4096).decode()

	client.send(convByte("\nEscreva o número da opção desejada:\n\n1 - Ver todas as publicações\n2 - Escrever uma nova publicação\n3 - Ler publicação\n4 - Apagar publicação\n5 - Se inscrever\n6 - Notificações\n7 - Sair\n"))

	if(True):
		while(True):
			opcao = client.recv(4096).decode()
			
			if(opcao == "1"):
				client.send(convByte(mostraPublicacoes()))

			elif(opcao == "2"):
				#Usuario digita titulo e conteúdo da publicação
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
				#Procura publicação digitada e se existir, printa ela na tela
				client.send(convByte("Escreva o título da publicação que deseja ler:\n"))
				titulo = client.recv(4096).decode()
				client.send(convByte(lerPublicacao(titulo)))
				continue

			elif(opcao == "4"):
				#Usuario digita nome da publicação e ele chama função pra encontrar e se existir, apagar
				client.send(convByte("Escreva o título da publicação que quer apagar:\n Obs.:Você só pode apagar uma publicação de sua autoria!\n"))
				titulo = client.recv(4096).decode()
				client.send(convByte(deletaPublicacao(titulo, usuario)))
				continue

			elif(opcao == "5"):
				#Printa o nome de todos os autores disponíveis para inscrição
				client.send(convByte("Nome dos autores que você pode se inscrever:")) 
				client.send(convByte(pegaNomes()))
				client.send(convByte("Em qual deseja se inscrever?"))
				autor = client.recv(4096).decode()
				client.send(convByte(salvaInscricao(autor, usuario)))
				continue

			elif(opcao == "6"):
				#Passa por todos os arquivos de inscrição e chama a função que gera notificação
				try:
					for root,dirs,files in os.walk(subscribe):
						for autor in files:
							client.send(convByte(geraNotificacao(usuario, autor)))
				except:
					client.send(convByte("Você não tem nenhuma notificação."))			
				continue

			elif(opcao == "7"):
				client.send(convByte("Desconectado."))
				print(str(ip) + " disconnected\n")
				return

publish = os.getcwd() + "\\Publicações\\"
subscribe = os.getcwd() + "\\Inscrições\\"

host = "127.0.0.1"
port = 33000
adress = (host, port)

if(not os.path.exists(publish)):
	os.system("mkdir Publicações")

if(not os.path.exists(subscribe)):
	os.system("mkdir Inscrições")

s = socket(AF_INET, SOCK_STREAM)
s.bind((host, port))
s.listen(1)
recebeConexoesThread(s)
