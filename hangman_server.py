from socket import *
import sys

import threading
import random
numClients = 0

def hangman(connectionSocket, addr, words):
    global numClients
    # print(numClients, "THREAD")
    clientMessage = connectionSocket.recv(1024).decode()
    guessWord = words[random.randint(0, 14)].lower()
    guessWord = guessWord[0:len(guessWord) - 1] #-1 to get rid of new line character
    lettersGuessed = []
    incorrectGuesses = []
    numIncorrect = 0
    # msg_flag = 0                    #msg_flag?
    wordLength = len(guessWord)

    if clientMessage == '0':    #need a better way to start game. tried sending empty message but doesn't work
        gameFinished = False
        msg = ""
        for x in range(wordLength):
            msg += '_'
        connectionSocket.send("{}{}{}{}"
                              .format(0, wordLength, numIncorrect, msg)
                              .encode())
    else:
        gameFinished = True

    while not gameFinished:
        clientMessage = connectionSocket.recv(1024).decode()
        # if(not clientMessage[0]):
        #     continue
        # if(clientMessage[1] and clientMessage[1] in lettersGuessed):
        #     connectionSocket.send("{}You already guessed this letter"
        #                           .format(chr(31))
        #                           .encode())
        #     continue
        if(not clientMessage):
            connectionSocket.close()
            lock.acquire()
            numClients -= 1
            lock.release()
            return
        if(clientMessage[1] and clientMessage[1] not in lettersGuessed):    #need to avoid the initial 'y' message that starts the game
            lettersGuessed.append(clientMessage[1])                         #i tried if clientmessage == "": continue, else:, but didn't work?
            if(clientMessage[1] not in guessWord):              
                numIncorrect += 1
                incorrectGuesses.append(clientMessage[1])
        msg = ""
        if(numIncorrect == 6):
            connectionSocket.send(
                            "{}{}".format(wordLength, guessWord).encode())
            connectionSocket.recv(1024)

            msg = "You Lose."
            gameFinished = True
            connectionSocket.send("{}{}"
                              .format(8, msg)
                              .encode())
            break
        for x in range(wordLength):
                if(guessWord[x] in lettersGuessed):
                    msg += guessWord[x]
                else:
                    msg += '_'
        if(msg == guessWord):
            connectionSocket.send("{}{}".format(wordLength, msg).encode())
            connectionSocket.recv(1024)
            connectionSocket.send("{}You Win!"
                                  .format(8)
                                  .encode())
            break
        for x in incorrectGuesses:
            msg += x
        connectionSocket.send("{}{}{}{}"
        .format(0, wordLength, numIncorrect, msg)       
        .encode())



    connectionSocket.close()
    lock.acquire()
    numClients -= 1
    lock.release()


with open('hangman_words.txt') as wordFile:
    words = wordFile.readlines()

serverPort = int(sys.argv[1])
seed = int(sys.argv[2])     #to control randomness, just input 0 or any integer doesn't matter
random.seed(seed)
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('127.0.0.1', serverPort))
serverSocket.listen()
print('The Server is ready to receive')
lock = threading.Lock()

while True:
    connectionSocket, addr = serverSocket.accept()
    lock.acquire()
    numClients += 1
    lock.release()
    if (numClients > 3):
        connectionSocket.recv(1024)
        connectionSocket.send("Nserver-overloaded".encode())
        connectionSocket.close()
        lock.acquire()
        numClients -= 1
        lock.release()
        continue

    clientGame = threading.Thread(target=hangman, args=(connectionSocket, addr, words))
    clientGame.start()
    # print(numClients, "MAIN")



