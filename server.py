from socket  import *
import os
from os.path import expanduser

def byt(text):
	return bytes(text, "utf-8")

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

def write():
    titulo = data.split(" ")[1]
	#texto = " ".join(data.split(" ")[2:])
    texto = data
    usuario="oi"
    if(novaPublicacao(titulo, usuario, texto)):
        conn.send(byt("Message successfully sent\n"))
    else:
        conn.send(byt("There was a problem in your message\n"))
        #continue


diretorio = os.getcwd() + "\\Blogs\\"
if(not os.path.exists(diretorio)):
	os.system("mkdir Blogs")





s = socket(AF_INET, SOCK_STREAM)
s.bind(("127.0.0.1", 10545))  #-
s.listen(1)           #-
(conn, addr) = s.accept()  # returns new socket and addr. client
while True:                # forever
  data = conn.recv(1024).decode()   # receive data from client
  if(not data): break       # stop if client stopped
  command = data.split(" ")[0]
  if (command == "write"):
      write()
conn.close()               # close the connection
