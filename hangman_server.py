from socket import *
import sys

import threading
import random


def hangman(connectionSocket, addr, words):
    clientMessage = connectionSocket.recv(1024).decode()
    guessWord = words[random.randint(0, 14)]
    lettersGuessed = []
    incorrectGuesses = []
    numIncorrect = 0
    wordLength = len(guessWord)

    if clientMessage.decod() == '0':
        gameFinished = False
    else:
        gameFinished = True

    while not gameFinished:
        if(clientMessage[1] and clientMessage[1] not in lettersGuessed):
            lettersGuessed.append(clientMessage[1])
            if(clientMessage[1] not in guessWord):
                numIncorrect += 1
                incorrectGuesses.append(clientMessage[1])
        if(numIncorrect == 6):
            connectionSocket.send("{}You Lose :(".format(chr(11)).encode())
        msg = ""
        for x in range(wordLength):
            if(guessWord[x] in lettersGuessed):
                msg += guessWord[x]
            else:
                msg += '_'
        if(msg == guessWord):
            connectionSocket.send("You Win!".encode(), msg.encode())
        for x in range(incorrectGuesses):
            msg += incorrectGuesses[x]
            
        connectionSocket.send("{}{}{}{}{}"
        .format(0, chr(wordLength), chr(numIncorrect), msg, incorrectGuesses)
        .encode())
    connectionSocket.close()
    numClients -= 1

with open('hangman_words.txt') as wordFile:
    words = wordFile.readlines()

serverPort = int(sys.argv[1])
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('127.0.0.1', serverPort))
serverSocket.listen()
print('The Server is ready to receive')
numClients = 0

while True:
    connectionSocket, addr = serverSocket.accept()

    if (numClients > 3):
        connectionSocket.send("000server-overloaded".encode())
        connectionSocket.close()

    numClients += 1
    clientGame = threading.Thread(hangman, (connectionSocket, addr, words))
    clientGame.start()


