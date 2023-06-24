# -*- coding: utf-8 -*-
__author__ = "Edson, Ismael, Marco Tulio"

import socket
import sys

HOST = '127.0.0.1'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1000000 # tamanho do buffer para recepção dos dados

def pegar_rota():
    rota = input("Informe a rota do arquivo: ")
    return rota

def receber_arquivo(s):
    with open("cliente.txt", "a") as arquivo:
        arquivo.truncate(0)

    rota = pegar_rota()
    s.sendto(rota.encode(), (HOST, PORT))
    print("Recebendo arquivo...")
    while True:
        data, _ = s.recvfrom(BUFFER_SIZE)
        texto_recebido = repr(data)
        texto_string = data.decode('utf-8')

        with open("cliente.txt", "a") as arquivo:
            arquivo.write(texto_string)

        if "Quantidade" in texto_string:
            linhas = texto_string.split("\n")
            print(linhas[-1])
            break

        if "error" in texto_string:
            print("Rota inválida!")
            break

def main(argv):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            print("Servidor executando!")
            receber_arquivo(s)
            opc = input("Deseja receber outro arquivo? (S/N)")

            while opc not in ["S", "N"]:
                opc = input("Deseja receber outro arquivo? (S/N)")

            while opc == "S":
                receber_arquivo(s)
                opc = input("Deseja receber outro arquivo? (S/N)")
                while opc not in ["S", "N"]:
                    opc = input("Deseja receber outro arquivo? (S/N)")

            close = "close"
            s.sendto(close.encode(), (HOST, PORT))
            print('Encerrando o socket cliente!')

    except Exception as error:
        print("Exceção - Programa será encerrado!")
        print(error)
        return

if __name__ == "__main__":
    main(sys.argv[1:])
