import random
import time

def greeter():
    print('Hi! What is your name?')
    name = input()
    gamesplayed = 0
    playerwins = 0
    computerwins = 0
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
    print("\nOK. Nice choice.")
    whostarts = random.choice([True, False])
    while True:
        if whostarts == True:
            firstgo = 'player'
        else:
            firstgo = 'computer'
        gamesplayed, playerwins, computerwins = start_game(name, gamesplayed, playerwins, computerwins, usertoken, pytoken, firstgo)
        whostarts = not whostarts
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

def start_game(name, gamesplayed, playerwins, computerwins, usertoken, pytoken, firstgo):
    gamesplayed += 1
    player = name
    print("...")
    print("Let's get this game started!\n")
    gameboard = {'top-L' : " ", 'top-M' : " ", 'top-R' : " ",
                 'mid-L' : " ", 'mid-M' : " ", 'mid-R' : " ",
                 'low-L' : " ", 'low-M' : " ", 'low-R' : " ",
                 }
    boardprint(gameboard)
    if firstgo == 'player':
        print('\nYou go first.\n')
    else:
        print('\nI will go first.\n')
    playerwins, computerwins = game(gameboard, usertoken, pytoken, firstgo, player, playerwins, computerwins)
    return(gamesplayed, playerwins, computerwins)

def game(gameboard, usertoken, pytoken, firstgo, player, playerwins, computerwins):
    goes = 0
    win = False
    if firstgo == 'player':
        while True:
            print("\nYour go...\n")
            time.sleep(1)
            turn = 'player'
            usergo(gameboard, usertoken, turn)
            goes += 1
            win = wincheck(gameboard, win)
            if win == True or goes == 9:
                break
            time.sleep(1)
            print("\nMy go...\n")
            time.sleep(1)
            turn = 'computer'
            pygo(gameboard, pytoken, turn)
            goes += 1
            win = wincheck(gameboard, win)
            if win == True or goes == 9:
                break
    else:
        while win != True:
            print("\nMy go...\n")
            time.sleep(1)
            turn = 'computer'
            pygo(gameboard, pytoken, turn)
            goes += 1
            win = wincheck(gameboard, win)
            if win == True or goes == 9:
                break
            print("\nYour go...\n")
            time.sleep(1)
            turn = 'player'
            usergo(gameboard, usertoken, turn)
            goes += 1
            win = wincheck(gameboard, win)
            if win == True or goes == 9:
                break
            time.sleep(1)
    if win == True and turn == 'player':
        print(f'Congratulations {player}, maybe we can play again?')
        playerwins += 1
    elif win == True and turn == 'computer':
        print('I won. Suck it!')
        computerwins += 1
    elif goes == 9:
        print('Ran out of turns. It is a stalemate.')
    return(playerwins, computerwins)

def boardprint(x):
    print(f" {x['top-L']} | {x['top-M']} | {x['top-R']} ")
    print('-----------')
    print(f" {x['mid-L']} | {x['mid-M']} | {x['mid-R']} ")
    print('-----------')
    print(f" {x['low-L']} | {x['low-M']} | {x['low-R']} ")

def usergo(gameboard, usertoken, turn):
    print("Where would you like to go? ('top-', 'mid-', 'low-' with 'L', 'M' or 'R')")
    #var = gameboard.keys()
    while True:
        pos = input()
        if pos not in gameboard.keys():
            print('I did not understand that. Please try again.')
        elif spacecheck(gameboard, pos, usertoken, turn) == True:
            break
        
def pygo(gameboard, pytoken, turn):
    # The computer identifies high-value moves (hotpicks) with the goodmoves() function. As long as there is at least 1 hotpick
    # move, the computer will pick its move from this list. It checks for instant-win moves too. 
    # If there are no high-value moves to play, it makes a random move of the free spaces.
    hotpicks = goodmoves(gameboard)
    if len(hotpicks) > 0:
        quickwin, pos = instawin(gameboard, hotpicks, pytoken)
        print(quickwin)
        if quickwin == False:
            pos = random.choice(hotpicks)
    else:
        while True:
            pos = random.choice(['top-', 'mid-', 'low-']) + random.choice(['L', 'R', 'M'])
            if gameboard[pos] == " ":
                break
    gameboard[pos] = pytoken
    boardprint(gameboard)
    return

def instawin(gameboard, hotpicks, pytoken):
    # This function looks at the "hotpick" moves identified by the goodmoves() function to check if any result in a win
    for pos in hotpicks:
        win = False
        gameboard[pos] = pytoken
        win = wincheck(gameboard, win)
        gameboard[pos] = " "
        if win == True:
            break
    if win == True:
        return(True, pos)
    else:
        return(False, "")
        
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

def goodmoves(gameboard):
    # This function is an abomination. 
    # It checks every winning line through every space on the board, to see if there are two matching tokens
    # in the winning line already. If two matching tokens are found, the third position is identified as a candidate. 
    # Candidates are then inspected to make sure they're empty, and empty candidate positions are returned as goodmoves.
    
    candidates = []
    goodmoves = []
    
    # top row good moves - identify if there is a space where 2 of 3 is present
    if gameboard['top-M'] == gameboard['top-R'] and gameboard['top-M'] != " " or gameboard['mid-M'] == gameboard['low-R'] and gameboard['mid-M'] != " " or gameboard['mid-L'] == gameboard['low-L'] and gameboard['mid-L'] != " ":
        candidates.append('top-L')
    
    if gameboard['top-L'] == gameboard['top-R'] and gameboard['top-L'] != " " or gameboard['mid-M'] == gameboard['low-M'] and gameboard['mid-M'] != " ":
        candidates.append('top-M')
    
    if gameboard['top-M'] == gameboard['top-L'] and gameboard['top-M'] != " " or gameboard['mid-M'] == gameboard['low-L'] and gameboard['mid-M'] != " " or gameboard['mid-R'] == gameboard['low-R'] and gameboard['mid-R'] != " ":
        candidates.append('top-R')
        
    # mid row good moves - identify if there is a space where 2 of 3 is present
    if gameboard['mid-M'] == gameboard['mid-R'] and gameboard['mid-M'] != " " or gameboard['top-L'] == gameboard['low-L'] and gameboard['top-L'] != " ":
        candidates.append('mid-L')
    
    if gameboard['mid-L'] == gameboard['mid-R'] and gameboard['mid-L'] != " " or gameboard['top-M'] == gameboard['low-M'] and gameboard['top-M'] != " " or gameboard['top-L'] == gameboard['low-R'] and gameboard['top-L'] != " " or gameboard['top-R'] == gameboard['low-L'] and gameboard['top-R'] != " ":
        candidates.append('mid-M')
    
    if gameboard['mid-M'] == gameboard['mid-L'] and gameboard['mid-M'] != " " or gameboard['top-R'] == gameboard['low-R'] and gameboard['top-R'] != " ":
        candidates.append('mid-R')
    
    # bottom row good moves
    if gameboard['low-M'] == gameboard['low-R'] and gameboard['low-M'] != " " or gameboard['mid-M'] == gameboard['top-R'] and gameboard['mid-M'] != " " or gameboard['mid-L'] == gameboard['top-L'] and gameboard['mid-L'] != " ":
        candidates.append('low-L')
    
    if gameboard['low-L'] == gameboard['low-R'] and gameboard['low-L'] != " " or gameboard['mid-M'] == gameboard['top-M'] and gameboard['mid-M'] != " ":
        candidates.append('low-M')
    
    if gameboard['low-M'] == gameboard['low-L'] and gameboard['low-M'] != " " or gameboard['mid-M'] == gameboard['top-L'] and gameboard['mid-M'] != " " or gameboard['mid-R'] == gameboard['top-R'] and gameboard['mid-R'] != " ":
        candidates.append('low-R')
    
    # Check candidates are empty
    for move in candidates:
        if gameboard[move] == " ":
            goodmoves.append(move)
    return(goodmoves)

greeter()