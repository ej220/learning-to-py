from random_word import RandomWords
import time

exec(open('hanged.py').read())

def greeter():
    print('Hi! What is your name?')
    name = input()
    gamesplayed = 0
    playerwins = 0
    print("Lets play Hangman.")
    while True:
        gamesplayed, playerwins = startgame(name, gamesplayed, playerwins)
        print(f'We have played {gamesplayed} games.\n')
        print(f"You have saved {playerwins} from the noose.")
        print(f"The Hangman has claimed {gamesplayed - playerwins}.\n")
        print('Play again? (yes/no)')
        if yesno() == False:
            break
    print('OK. It was nice playing with you. See you next time!')

def yesno():
    while True:
        response = input()
        if response[0].lower() not in ['y', 'n']:
            print('I am sorry, I did not understand that. Try again please. (yes / no)')
        elif response[0].lower() == 'n':
            return(False)
        else:
            return(True)

def startgame(name, gamesplayed, playerwins):
    gamesplayed += 1
    print("\nI'm thinking of a word...\n")
    time.sleep(1)
    word = f_wordget()
    print("Got one!\n")
    print("Let's play!\n\n")
    playerwins = game(name, word, playerwins)
    return(gamesplayed, playerwins)

def game(name, word, playerwins):
    clue = "_" * len(word)
    print(clue)
    guesses = ""
    badguesses = 0
    goodguesses = 0
    
    while badguesses < 10:
        print("\nTake a guess at a letter....\n")
        guess, guesses = f_guess(guesses)
        let = []
        goodguess = False

        for l in range(len(word)):
            if guess == word[l]:
                goodguess = True
                goodguesses += 1
                let.append(l)

        if goodguess != True:
            print("Tough luck, try again!")
            badguesses += 1
        else:
            print("Good guess, you've got " + str(goodguesses) + " out of " + str(len(word)) + " letters correct.")
            for i in let:
                newclue = clue[:(i)] + guess + clue[(i+1):]
                clue = newclue

    
        print(f"You have guessed the letters{guesses}")
        print("You have " + str(10 - badguesses) + " lives left.")
        print("")
        print("")
        print(clue)
        hanged(badguesses)
        print("")
        if goodguesses == len(word):
            break
    
    if badguesses == 10:
        print(f"The word was {word}\n")
        print(f"Tough luck, {name}. Try again next time")
    else:
        print(f"Congratulations, {name}!")
        print(f"The word was {word}.")
        print("You won!")
        playerwins += 1
    return(playerwins)

def f_wordget():
    while True:
        word = RandomWords().get_random_word()
        if f_wordcheck(word) == True:
            word = word.lower()
            break
    return (word) 

def f_wordcheck(word):
    for char in word:
        if char.isalpha() != True:
            return(False)
    return(True)


def f_guess(guesses):
    while True:
        thisguess = input()
        if len(thisguess) != 1:
            print("Please guess a single letter.")
        elif thisguess.isalpha() != True:
            print("Letters only please.")
        elif thisguess in guesses:
            print(f"You've already guessed the letter {thisguess}. Try again.")
        else:
            guess = thisguess.lower()
            guesses = guesses + ", " + guess
            break
    return(guess, guesses)

greeter()