from socket import *
import sys

serverName = sys.argv[1]
serverPort = int(sys.argv[2])
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
message = input('P')
clientSocket.send(message.encode())
serverMessage = clientSocket.recv(1024)
print(serverMessage.decode())
clientSocket.close()
