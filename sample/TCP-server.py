from socket import *


serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM) # create TCP welcoming socket
serverSocket.bind(('', serverPort))

serverSocket.listen(1) # server begins listening for in coming TCP requests
print('The server is ready to receive')
while True: # loop forever
    connectionSocket, addr = serverSocket.accept() # server waits on accept() for incoming requests, new socket created on return
    sentence = connectionSocket.recv(1024).decode() # read bytes from socket
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence.encode())

    connectionSocket.close()