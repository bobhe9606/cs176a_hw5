from socket import *
import sys

serverName = sys.argv[1]
serverPort = int(sys.argv[2])
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
message = input('Ready to start game? (y/n): ')
if message == 'y':
    clientSocket.send('0')
else:
    print('Game Over!')

while True:
    zero, wordLength, numIncorrect, msg, incorrectGuesses = clientSocket.recv(1024)
    print(msg.decode())
    print('Incorrect Guesses: ', incorrectGuesses.decode(), '\n')

    letter = input('Letter to guess: ')
    clientSocket.send(letter.encode())
    status, msg = clientSocket.recv(1024)
    status = status.decode()
    msg = msg.decode()
    if(status == "You Win!"):
        print('The word was ', msg)
        print(status)
        print("Game Over!")
    elif(status== "You Lose :("):
        print(status)
        print('Game Over!')







clientSocket.send(message.encode())
serverMessage = clientSocket.recv(1024)
print(serverMessage.decode())
clientSocket.close()
