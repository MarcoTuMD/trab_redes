# -*- coding: utf-8 -*-
__author__ = "Edson, Ismael, Marco Tulio"

import socket, sys
from threading import Thread
import time


HOST = '127.0.0.1'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1000000  # tamanho do buffer para recepção dos dados

def enviar_arquivo(clientsocket,addr):
    try:
        while True:
            cont_linhas = 0
            data = clientsocket.recv(BUFFER_SIZE)
            inicio = time.time()
            rota = data.decode('utf-8') 
            print('recebido do cliente {} na porta {}: {}'.format(addr[0], addr[1],rota))

            if (rota == 'close'):
                print('vai encerrar o socket do cliente {} !'.format(addr[0]))
                clientsocket.close() 
                return 

            with open(rota, "r") as arquivo:
                linhas = arquivo.readlines()
                for linha in linhas:
                    linha_encode = linha.encode()
                    clientsocket.send(linha_encode)
                    cont_linhas+=1
                
            fim = time.time()
            end = "Quantidade de linhas: {} |||| tempo de execucao: {}".format(cont_linhas,  round(fim - inicio, 3))
            clientsocket.send(end.encode())
    except Exception as error:
        print("Erro na execução do servidor!!")
        end = "error"
        clientsocket.send(end.encode())
        print(error)   
        enviar_arquivo(clientsocket,addr)     

def main(argv):
    try:
        # AF_INET: indica o protocolo IPv4. SOCK_STREAM: tipo de socket para TCP,
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
            while True:
                server_socket.listen()
                clientsocket, addr = server_socket.accept()
                print('Conectado ao cliente no endereço:', addr)
                t = Thread(target=enviar_arquivo, args=(clientsocket,addr))
                t.start()   
    except Exception as error:
        print("Erro na execução do servidor!!")
        print(error)        
        return             



if __name__ == "__main__":   
    main(sys.argv[1:])