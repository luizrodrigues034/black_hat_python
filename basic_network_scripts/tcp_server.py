import socket
import threading
IP = "0.0.0.0"
PORT = 9998

def main():
    #Criand socket e espeficicando as conexoes
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #.bind para definir qual ip e servidor o servidor vai estar escutando
    server.bind((IP, PORT))
    #.listen definir o backlog de conexoes que nosso servidor vai ser capaz de escutar
    server.listen(5)
    print(f"[*] Servidor esta ativo, escutando no {IP} na porta {PORT}")
    
    #Estabelecemos um loop infinito paa manter o servidor ativo
    while True:
        
        #Conexao estabelecida com cliente
        client,addr = server.accept()

        print(f"[*] Conexao aceita de {addr[0]}:{addr[1]}")
        #Criacao da thread
        client_handler = threading.Thread(target=handler_client, args=(client,))
        
        #Habilitando a thread para lidar com a conexao do usuario
        client_handler.start()
        
        
    
    #funcao responsavel por receber o conteudo da conexao e responder
def handler_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f"[*] Recebido: {request.decode("utf-8")}")
        sock.send(b"ACK")
    
if __name__ == '__main__':
    main()
