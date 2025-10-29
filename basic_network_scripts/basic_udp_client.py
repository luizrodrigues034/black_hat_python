#Na sua maquina execute:nc -l -u 9997

import socket
print("run")
target_host = "127.0.0.1"
target_port = 9997

#Indicamos que sera um host com edereco ipv4, e com SOCK_DGRAM informando que a conexao ser udp
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.sendto(b"ABCDEFGHIJ",(target_host, target_port))

data, addr = client.recvfrom(4096)

print(data.decode)
print(addr)
client.close()