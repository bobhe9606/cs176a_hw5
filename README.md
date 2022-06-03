# Nicolas Johnson and Robert He

#Operation

Hangman Client establishes a connection with Hangman Server to start the game. The server is able to manage a maximum of 3 clients at any given time, each will be playing their own game. The server will respond to every incoming guess, which can only be character variable, and respond with a feedback message to every guess. In the feedback message, the program will keep track of which letters were guessed correctly and the incorrect guesses made. If the input guess has a length greater than 1 or is a numeric value, the program will output an error message and allow for a re-guess. The game will continue until the word is guessed correctly or the guess limit of 6 is exceeded, and the final word will be revealed in the end.





