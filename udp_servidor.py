# -*- coding: utf-8 -*-
__author__ = "Edson, Ismael, Marco Tulio"

import socket
import sys
from threading import Thread
import time

HOST = '127.0.0.1'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1000000  # tamanho do buffer para recepção dos dados

def enviar_arquivo(data, addr, server_socket):
    try:
        cont_linhas = 0
        inicio = time.time()
        rota = data.decode('utf-8')
        print('Recebido do cliente {} na porta {}: {}'.format(addr[0], addr[1], rota))

        if (rota == 'close'):
            print('Vai encerrar o socket do cliente {}!'.format(addr[0]))
            return

        with open(rota, "r") as arquivo:
            linhas = arquivo.readlines()
            for linha in linhas:
                linha_encode = linha.encode()
                server_socket.sendto(linha_encode, addr)
                if cont_linhas % 100 == 0:
                    time.sleep(0.001)
                cont_linhas += 1
                
                
        fim = time.time()
        end = "Quantidade de linhas: {} |||| Tempo de execução: {}".format(cont_linhas, round(fim - inicio, 3))
        server_socket.sendto(end.encode(), addr)
    except Exception as error:
        print("Erro na execução do servidor!")
        end = "error"
        server_socket.sendto(end.encode(), addr)
        print(error)

def main(argv):
    try:
        UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPServerSocket.bind((HOST, PORT))
        while True:
            bytesAddressPair = UDPServerSocket.recvfrom(BUFFER_SIZE)
            mensagem = bytesAddressPair[0]
            endereco = bytesAddressPair[1]
            print('Conectado ao cliente no endereço:', endereco)
            enviar_arquivo(mensagem, endereco, UDPServerSocket)
    except Exception as error:
        print("Erro na execução do servidor!")
        print(error)
        return

if __name__ == "__main__":
    main(sys.argv[1:])
