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
    msg_flag = 0                    #msg_flag?
    wordLength = len(guessWord)

    if clientMessage == 'y':    #need a better way to start game. tried sending empty message but doesn't work
        gameFinished = False
    else:
        gameFinished = True

    while not gameFinished:
        if(clientMessage[0] and clientMessage[0] not in lettersGuessed):    #need to avoid the initial 'y' message that starts the game
            lettersGuessed.append(clientMessage[0])                         #i tried if clientmessage == "": continue, else:, but didn't work?
            if(clientMessage[0] not in guessWord):              
                numIncorrect += 1
                incorrectGuesses.append(clientMessage[0])
        msg = ""
        if(numIncorrect != 6):
            for x in range(wordLength):
                if(guessWord[x] in lettersGuessed):     #need to fix this to correspond correct letter positions
                    msg += guessWord[x]
                else:
                    msg += '_'
            msg += '\n'
            msg += 'Incorrect Guesses: '
            for x in incorrectGuesses:
                msg += x +  ' '          
            msg += '\n'
            if(msg == guessWord):
                msg = "You Win!" + "\n" + "The word was " + guessWord
                gameFinished = True
        if(numIncorrect == 6):
            msg = "You Lose :(" + "\n" + "The word was " + guessWord
            gameFinished = True
        connectionSocket.send("{}{}{}{}"
        .format(msg_flag, chr(wordLength), chr(numIncorrect), msg)       
        .encode())

        clientMessage = connectionSocket.recv(1024).decode()


    connectionSocket.close()


with open('hangman_words.txt') as wordFile:
    words = wordFile.readlines()

serverPort = int(sys.argv[1])
seed = int(sys.argv[2])     #to control randomness, just input 0 or any integer doesn't matter
random.seed(seed)
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
    clientGame = threading.Thread(target=hangman, args=(connectionSocket, addr, words,))
    clientGame.start()
    numClients -= 1



