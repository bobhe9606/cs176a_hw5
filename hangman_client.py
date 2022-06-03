from socket import *
import sys

from pyrsistent import inc

word = ""
serverName = sys.argv[1]
serverPort = int(sys.argv[2])
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
message = input('Ready to start game? (y/n): ')
if message == 'y':
    clientSocket.send("0".encode())
    start = True
    msg = clientSocket.recv(1024).decode()

    wordLength = int(msg[1])
    numIncorrect = int(msg[2])
    word = msg[3:3 + wordLength]
    wrongLetters = ""

    printWord = ""
    for x in range(len(word) - 1):
            printWord += word[x] + " "
    printWord += word[-1]
    print(printWord)
    print("Incorrect Guesses: " + wrongLetters + "\n")
    letter = input('Letter to guess: ')
    while(len(letter) > 1 or letter.isdigit() or len(letter) < 1):
        print('Error! Please guess one letter.')
        letter = input('Letter to guess: ')

    letter = letter.lower()
    clientSocket.send("1{}".format(letter).encode())


else:
    start = False

while start:
    msg = clientSocket.recv(1024).decode() 
    if msg ==  "":
        continue
    else:
        msg_flag = msg[0]

        if(msg_flag != '0'):

             if(msg.find("You Lose") != -1):
                print(msg[1:])
                start = False
                break
             else:
                 finalWord = ""
                 word = msg[1:]
                 for x in range(len(word) - 1):
                    finalWord += word[x] + " "
                 finalWord += word[-1]
                 print("THe word was " + finalWord)
                 clientSocket.send("0".encode())
                 msg = clientSocket.recv(1024).decode()
                 print(msg[1:])
                 start = False
                 break
        else:
            wordLength = int(msg[1])
            numIncorrect = int(msg[2])
            word = msg[3:3 + wordLength]
            if(numIncorrect != 0):
                incorrectGuesses = msg[3 + wordLength:]
                wrongLetters = ""
                for x in range(len(incorrectGuesses) - 1):
                    wrongLetters += incorrectGuesses[x] + " "
                wrongLetters += incorrectGuesses[-1]
            printWord = ""
            for x in range(len(word) - 1):
                printWord += word[x] + " "
            printWord += word[-1]
    print(printWord)
    print("Incorrect Guesses: " + wrongLetters + "\n")
    letter = input('Letter to guess: ')
    while(len(letter) > 1 or letter.isdigit() or len(letter) < 1):
        print('Error! Please guess one letter.')
        letter = input('Letter to guess: ')

    letter = letter.lower()
    # print(letter)
    # print(int(numIncorrect, 10))         #not returniing numIncorrect
    clientSocket.send("1{}".format(letter).encode())





print("Game Over!")
clientSocket.close()

