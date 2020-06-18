#!/bin/python3.8

# This script is a game of Hangman, written in Python
from random_word import RandomWords
import string
letters = string.ascii_lowercase + string.ascii_uppercase
r = RandomWords()

def func_wordGet():
    while True:
        word = r.get_random_word()
        for char in word:
            if char.isalpha() == False:
                Letters = False
            else:
                Letters = True
        if Letters == True:
            word = word.lower()
            break
    return (word)  

Guesses = ""
def func_guess():
    global Guesses
    while True:
        goodGuess = True
        guess = input()
        if len(guess) == 1:
            for char in guess:
                if char.isalpha() == False or char == " ":
                    print("Letters only please.")
                    goodGuess = False
                if char in Guesses:
                    print("You have already that letter, try again.")
                    goodGuess = False
        else:
            print("One letter at a time please.")
            goodGuess = False
        guess = guess.lower()
        if goodGuess != False:
            Guesses = Guesses + guess + ", "
            break
    return (guess)

print("Hi there! What is your name?")
name = input()
print("Nice to meet you, " + name + ". Lets play a game of hangman.")
word = func_wordGet()
print("I am thinking of a word. It is " + str(len(word)) + " letters long." )
clue = len(word) * "_"
print(clue)

BadGuesses = 0
GoodGuesses = 0
Guesses = ""

while BadGuesses < 10:
    print("Take a guess at a letter....")
    guess = func_guess()
    let = []
    goodGuess = False

    for l in range(len(word)):
        if guess == word[l]:
            goodGuess = True
            GoodGuesses = GoodGuesses + 1
            let.append(l)

    if goodGuess != True:
        print("Tough luck, try again!")
        BadGuesses = BadGuesses + 1
    else:
        print("Good guess, you've got " + str(GoodGuesses) + " out of " + str(len(word)) + " letters correct.")
        for i in let:
            newclue = clue[:(i)] + guess + clue[(i+1):]
            clue = newclue

    print(clue)
    print("You have guessed " + Guesses)
    print("You have " + str(10 - BadGuesses) + " lives left.")
    if GoodGuesses == len(word):
        break

if BadGuesses == 10:
    print("The word was " + word)
    print("Tough luck. Try again next time")
else:
    print("Congratulations!")
    print("You won the game!")
