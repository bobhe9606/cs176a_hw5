from socket import *
import sys

serverName = sys.argv[1]
serverPort = int(sys.argv[2])
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
message = input('Ready to start game? (y/n): ')
if message == 'y':
    clientSocket.send(message.encode())
    start = True
else:
    print('Game Over!')
    start = False

while start:
    zero, wordLength, numIncorrect, msg, incorrectGuesses = clientSocket.recv(1024)
    print(msg.decode())
    print('Incorrect Guesses: ', incorrectGuesses.decode(), '\n')

    letter = input('Letter to guess: ')
    letter = letter.encode()
    while(len(letter) > 1 or letter.isdigit()):
        print('Error! Please guess one letter')
        letter = input('Letter to guess: ')
        letter = letter.encode()

    letter = letter.lower()
    clientSocket.send(letter)
    status, msg = clientSocket.recv(1024)
    status = status.decode()
    msg = msg.decode()
    if(status == "You Win!"):
        print('The word was ', msg)
        print(status)
        print("Game Over!")
        start =  False
    elif(status== "You Lose :("):
        print(status)
        print('Game Over!')
        start =  False

clientSocket.close()







clientSocket.send(message.encode())
serverMessage = clientSocket.recv(1024)
print(serverMessage.decode())
clientSocket.close()