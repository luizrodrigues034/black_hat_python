import argparse #Lidar com argumentos de linha de comando
import socket #lidar com as conexoes
import shlex # faz o parse de strings no estilo shell separando o argumento e comandos
import subprocess # Permite executar comandos externo e interagir com outros programas do sistema
import sys # fornece acesso aos recusos do interpretador python
import textwrap # utilizado para quebrar texto em linhas com larguras controloadas
import threading # Lidar com multi processos

def execute(cmd):
    #Estamos utilizando o modulo para definir o nosso menu help, e definir os comandos que estao disponiveis
    parser = argparse.ArgumentParser(description="BHP Net Tool",
    formatter_class=argparse.RawDescriptionHelpFormatter,epilog=textwrap.dedent("""
     Exemplo:
     netcat.py -t <TARGET_IP> -p <PORTa> -l c #shell de comando
     netcat.py -t <TARGET_IP> -p <PORTa> -l -u=file.txt #fazer upload de arquivo
     netcat.py -t <TARGET_IP> -p <PORTa> -l -e=\"cat /etc/passwd\" #executar comando

     echo 'ABC' | ./netcat.py -t <TARGET_IP> -p <PORTa>  #enviar texto para porta
     netcat.py -t <TARGET_IP> -p <PORTa> #conectar ao servidor
     """))

    parser.add_argument('-c', '--command', action='store_true', help="shell de comando")
    parser.add_argument('-e', '--execute', help='executar comando especificado')
    parser.add_argument('-l', '--listen', action='store_true', help="escutar")
    parser.add_argument('-p', '--port', type=int, default=5555, help="especifica porta")
    parser.add_argument("-t", "--target", default="192.168.100.228", help="especificar o alvo")
    parser.add_argument("-u", "--upload", help="Fazer upload de um arquivo")

    args= parser.parse_args() # Le os argumentos do terminal

    if args.listen:
        buffer= ""
    else: 
        buffer = sys.stdin.read()
    nc = NetCat(args, buffer.encode())
    nc.run()

    #Classe NetCat, tem como parametros:args, buffer
    #args: Argumentos passados ao script ser chamado
    #buffer: Parametro opcional para enviar conteudo durante a conexao
class NetCat:
    def __init__(self, args, buffer= None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #setsockopt(level,option, value)
        #setsockopt -> alterar as opcoes de funcionamento do socket, ou seja como o socket ira se comportar
        #level-> em qual camda a opcao sera aplicada, SOL_SOCKET -> nivel de socket; 
        #option -> como a conexao vai se comportar, SO_REUSEADDR -> permite usar o mesmo endereco e porta sem esperaro tmeout do sistema.
        #value -> ovalor(0 ou 1 para desligar e ligar)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        
    def run(self):
        #Caso tenha selecionado listen..., caso nao é para envio
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):
        #estabelecemo a conexao com o host definido
        self.socket.connect((self.args.target, self.args.port))
        #Se o buffer nao for vazio
        if self.buffer:
            self.socket.send(self.buffer)
        
        try:
            while True:
                recv_len = 1
                response = b''
                #O recv_len foi definido como um so para entrar no laco
                while recv_len:
                    #le ate 4096 bytes
                    data = self.socket.recv(4096)
                    #recebe o tamanho
                    recv_len = len(data)
                    #recebe o valor para futura exibicao da esposta
                    response += data.decode()
                    #quando for menor, signifca que nao tem mais dados para ser enviado
                    if recv_len < 4096:
                        break

                if response:
                    #exibe a ultima resposta
                    print(response)
                    #O processo de shell inicia em loop ate ser encerrado
                    buffer = input("> ")
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print("Interrompido pelo usuário")
            self.socket.close()
            sys.exit()
