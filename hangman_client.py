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
    msg = clientSocket.recv(1024).decode() 
    if msg ==  "":
        continue
    else:
        msg_flag = msg[0]
        wordLength = msg[1]
        numIncorrect = msg[2]
        msg = msg[4:]
    print(msg)

    if(numIncorrect == 6):
        start = False
        break
    if(msg.find("You Win!") != -1):
        start = False
        break

    letter = input('Letter to guess: ')
    while(len(letter) > 1 or letter.isdigit() or len(letter) < 1):
        print('Error! Please guess one letter')
        letter = input('Letter to guess: ')

    letter = letter.lower()
    print(letter)
    print(numIncorrect)         #not returniing numIncorrect
    clientSocket.send(letter.encode())





print("Game Over!")
clientSocket.close()

