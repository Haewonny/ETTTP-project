from socket import *

servername = '127.0.0.1'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM) # create TCP socket for server
clientSocket.connect((servername, serverPort))
sentence = input('Input lowercase sentence : ')
clientSocket.send(sentence.encode())

modifiedSentence = clientSocket.recv(1024) # No need to attach server name, port
print('From Server : ', modifiedSentence.decode())
clientSocket.close()