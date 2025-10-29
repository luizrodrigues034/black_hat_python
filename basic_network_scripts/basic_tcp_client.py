import socket

target_host = "www.google.com"
target_port = 80

#Estamos criando um objeto socket e passando como parametro o 
#AF.INET que indica que utilizaremos um endereço ou no nome de umost ipv4
#sock_stream indicando um cliente TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Realizaos a conexao do cliente com o servidor
client.connect((target_host, target_port))

client.send(b"GET / HTTP/1.1\r\nHost: google.com \r\n\r\n")

response = client.recv(4096)

print(response.decode())

client.close()
