import random
import time

def greeter():
    print('Hi! What is your name?')
    name = input()
    gamesplayed = 0
    playerwins = 0
    computerwins = 0
    while True:
        gamesplayed, playerwins, computerwins = start_game(name, gamesplayed, playerwins, computerwins)
        print(f'We have played {gamesplayed} games.')
        print(f'The current score is: You {playerwins} - {computerwins} Me')
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

def start_game(name, gamesplayed, playerwins, computerwins):
    gamesplayed += 1
    player = name
    print("Lets play noughts and crosses. Pick a token, X or O.")
    while True:
        pick = input()
        if pick.lower() == "x":
            usertoken = "X"
            pytoken = "O"
            break
        elif pick.lower() == "o":
            usertoken = "O"
            pytoken = "X"
            break
        else:
            print('Pick again, I did not understand that.')
    print("")
    print("OK. Nice choice.")
    print("...")
    print("Let's get this game started!")
    print("")
    gameboard = {'top-L' : " ", 'top-M' : " ", 'top-R' : " ",
                 'mid-L' : " ", 'mid-M' : " ", 'mid-R' : " ",
                 'low-L' : " ", 'low-M' : " ", 'low-R' : " ",
                 }
    boardprint(gameboard)
    print("")
    firstgo = random.choice(['player', 'computer'])
    if firstgo == 'player':
        print('You go first.')
    else:
        print('I will go first.')
    print("")
    playerwins, computerwins = game(gameboard, usertoken, pytoken, firstgo, player, playerwins, computerwins)
    return(gamesplayed, playerwins, computerwins)

def game(gameboard, usertoken, pytoken, firstgo, player, playerwins, computerwins):
    goes = 0
    win = False
    if firstgo == 'player':
        while True:
            print("")
            print("Your go...")
            print("")
            time.sleep(1)
            turn = 'player'
            usergo(gameboard, usertoken, turn)
            goes += 1
            win = wincheck(gameboard, win)
            if win == True or goes == 9:
                break
            time.sleep(1)
            print("")
            print("My go...")
            print("")
            time.sleep(1)
            turn = 'computer'
            pygo(gameboard, pytoken, turn)
            goes += 1
            win = wincheck(gameboard, win)
            if win == True or goes == 9:
                break
    else:
        while win != True:
            print("")
            print("My go...")
            print("")
            time.sleep(1)
            turn = 'computer'
            pygo(gameboard, pytoken, turn)
            goes += 1
            win = wincheck(gameboard, win)
            if win == True or goes == 9:
                break
            print("")
            print("Your go...")
            print("")
            time.sleep(1)
            turn = 'player'
            usergo(gameboard, usertoken, turn)
            goes += 1
            win = wincheck(gameboard, win)
            if win == True or goes == 9:
                break
            time.sleep(1)
    if win == True:
        if goes % 2 != 0 and firstgo == 'player':
            print('Congratulations ' + player + '. Maybe we can play again?')
            playerwins += 1
        elif goes % 2 == 0 and firstgo == 'computer':
            print('Congratulations ' + player + '. Maybe we can play again?')
            playerwins += 1
        else:
            print('I won. Suck it!')
            computerwins += 1
    elif goes == 9:
        print('Ran out of turns. It is a stalemate.')
    return(playerwins, computerwins)

def boardprint(x):
    print(' ' + str(x['top-L']) + ' | ' + str(x['top-M']) + ' | ' + str(x['top-R']) + ' ')
    print('-----------')
    print(' ' + str(x['mid-L']) + ' | ' + str(x['mid-M']) + ' | ' + str(x['mid-R']) + ' ')
    print('-----------')
    print(' ' + str(x['low-L']) + ' | ' + str(x['low-M']) + ' | ' + str(x['low-R']) + ' ')

def usergo(gameboard, usertoken, turn):
    print("Where would you like to go? ('top-', 'mid-', 'low-' with 'L', 'M' or 'R')")
    while True:
        pos = input()
        goodrow = ["top-", 'mid-', 'low-']
        goodcol = ['L', 'M', 'R']
        if pos[:3] not in goodrow and pos[-1] not in goodcol:
            print('I did not understand that. Please try again.')
        elif spacecheck(gameboard, pos, usertoken, turn) == True:
            break
        
def pygo(gameboard, pytoken, turn):
    while True:
        pos = random.choice(['top-', 'mid-', 'low-']) + random.choice(['L', 'R', 'M'])
        #print(pos)
        if spacecheck(gameboard, pos, pytoken, turn) == True:
            break
    return

def spacecheck(gameboard, pos, token, turn):
    if gameboard[pos] == " ":
        gameboard[pos] = token
        boardprint(gameboard)
        return(True)
    elif turn == 'player':
        print("This space is occupied. Try again")

def wincheck(gameboard, win):
    # Check rows
    for row in ['top-', 'mid-', 'low-']:
        if gameboard[row + 'L'] == gameboard[row + 'M'] and gameboard[row + 'M'] == gameboard[row + 'R']:
            if gameboard[row + 'M'] != " ":
                win = True
    # Check columns
    for col in ['-L', '-M', '-R']:
        if gameboard['top' + col] == gameboard['mid' + col] and gameboard['mid' + col] == gameboard['low' + col]:
            if gameboard['mid' + col] != " ":
                win = True
    # Check diaganols
    if gameboard['mid-M'] != " ":
        if gameboard['mid-M'] == gameboard['top-L'] and gameboard['mid-M'] == gameboard['low-R']:
            win = True
        if gameboard['mid-M'] == gameboard['low-L'] and gameboard['mid-M'] == gameboard['top-R']:
            win = True
    return(win)

greeter()