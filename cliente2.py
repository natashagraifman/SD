import socket
from threading import Thread
import time

def recebe_mensagens(socket_):
    while True:
        msg = socket_.recv(1024)
        if not(len(msg)):
            break
        print(msg.decode("utf-8"))
    print("Conexão com o servidor encerrada")


def envia_mensagens(socket_):
    while True:
        msg = input("Msg> ")
        try:
            socket_.sendall(msg.encode("utf-8"))
        except socket.error:
            break
        if msg.lower() == "fim":
            socket_.close()
            break
    print("Envio de mensagens encerrado!")


def client(h, p):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4,tipo de socket
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    envia = Thread(target=envia_mensagens, args=(s,))
    recebe = Thread(target=recebe_mensagens, args=(s,))

    envia.start()
    recebe.start()

    while threang.active_count() > 1:
        # pausa de 0.1 segundo,
        # Evita que a CPU fique processando a comparação acima sem parar.
        time.sleep(0.1)
    print("Programa encerrado")


if __name__ == '__main__':
    h = input("Host do servidor: ")
    p = input("Porta do servidor: ")
    client(h, p)
