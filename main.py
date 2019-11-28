import random
from game import Game
from humanplayer import HumanPlayer
from aiplayer import AIPlayer
from action_card import ActionCard
from normal_card import NormalCard
from functions import format_card
from os import system, name
from time import sleep
if name == "nt": import msvcrt
else: import sys, termios

colors = ["\033[31m" + "Red" + "\033[0m",
          "\033[32m" + "Green" + "\033[0m",
          "\033[33m" + "Yellow" + "\033[0m",
          "\033[34m" + "Blue" + "\033[0m"]
wild_color = "\033[31m" + "W" + "\033[0m" + "\033[32m" + "i" + "\033[0m" + "\033[33m" + "l" + "\033[0m" + "\033[34m" + "d" + "\033[0m"
actions = ["Block", "Reverse", "Draw two"]
wild_actions = ["Wild", "Wild Draw Four"]

# Create deck
deck = [NormalCard(color, num) for num in range(0, 10) for color in colors]
deck += [NormalCard(color, num) for num in range(1, 10) for color in colors]
deck += [ActionCard(color, action) for action in actions for color in colors] * 2
deck += [ActionCard(wild_color, wild_action) for wild_action in wild_actions] * 4

random.shuffle(deck)

game = Game(deck)

game.create_pile()

result = None

if name == "nt": result = system("cls")
else: result == system("clear")

while True:
    human_player_count = None
    try:
        human_player_count = int(input("How many people are going to play? (Up to 5 players, including AI)\n"))
    except ValueError:
        print("{0} is not a number...\n".format(human_player_count))
        continue
    
    if human_player_count < 0:
        print("The number you entered ({0}) is a negative number. I can't use those.\n".format(human_player_count))
        continue

    if human_player_count > 5:
        print("The number you entered ({0}) is too big.\n".format(human_player_count))
        continue

    ai_player_count = None 
    try:
        ai_player_count = int(input("How many AI players do you want? (Up to 5 players, including normal players)\n"))
    except ValueError:
        print("{0} is not a number...\n".format(ai_player_count))
        continue

    if human_player_count + ai_player_count > 5:
        print("The amount of real players and AI players is too big.\n")
        continue

    elif human_player_count + ai_player_count == 0:
        print("Do you really want to start a game with 0 players? I don't think so.\n")
        continue

    elif human_player_count + ai_player_count < 0:
        print("The amount of real players and AI players is a negative number. ???\n")
        continue

    for i in range(0, human_player_count):
        human_player = HumanPlayer()
        human_player.draw_cards(7, game)
        game.add_player(human_player)
    
    for i in range(0, ai_player_count):
        ai_player = AIPlayer()
        ai_player.draw_cards(7, game)
        game.add_player(ai_player)

    break

turn = 0
while True:
    plr = game.players[turn]
    print("-" * 75)
    print("TOP CARD:")
    print("-" * 75)
    print(format_card(game.pile[0]))

    plr.play(game)
    print("-" * 75)
    print("PILE:")
    print("-" * 75)

    for card in game.pile:
        print(format_card(card))
    print("-" * 75)

    if type(plr) == HumanPlayer:
        print("-" * 75)
        print("HAND:")
        print("-" * 75)
        for card in plr.hand:
            print(format_card(card))
        print("-" * 75)

    enter_message = "Press Enter to end turn"
    next_player = None
    try:
        next_player = game.players[turn + 1]
    except IndexError:
        next_player = game.players[0]

    if type(next_player) == AIPlayer:
        enter_message += " (Next player is an AI)"
    input(enter_message)


    for i in reversed(range(1, 6)):
        if name == "nt":
            while msvcrt.kbhit():
                msvcrt.getch()
        else:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)
        print("Switching to next player in {0}...".format(str(i)), end="\r")
        sleep(1)

    if len(game.players) - 1 == turn:
        turn = 0
    else:
        turn += 1
    if name == "nt": result = system("cls")
    else: result == system("clear")


