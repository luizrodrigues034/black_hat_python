import socket
import time

time.sleep(10)
target_host = "127.0.0.0"
target_port = 9998

#Estamos criando um objeto socket e passando como parametro o 
#AF.INET que indica que utilizaremos um endereço ou no nome de umost ipv4
#sock_stream indicando um cliente TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Realizaos a conexao do cliente com o servidor
client.connect((target_host, target_port))

client.send(b"Hello")

response = client.recv(4096)

print(response.decode("utf-8"))

client.close()
