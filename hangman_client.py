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
    msg = clientSocket.recv(1024)   
    msg = msg.decode()
    #print(msg)
    if msg ==  "":
        continue
    else:
        msg_flag = msg[0]
        wordLength = msg[1]
        numIncorrect = msg[2]
        msg = msg[3:]

    if(numIncorrect == 6):
        start = False
        break
    if(msg.find("You Win!") != -1):
        start = False
        break

    letter = input('Letter to guess: ')
    letter = letter.encode()
    while(len(letter) > 1 or letter.isdigit()):
        print('Error! Please guess one letter')
        letter = input('Letter to guess: ')
        letter = letter.encode()

    letter = letter.lower()
    clientSocket.send(letter)





print("Game Over!")
clientSocket.close()

