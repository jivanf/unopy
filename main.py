from random import shuffle
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
wild_color = ("\033[31m" + "W" + "\033[0m" + 
              "\033[32m" + "i" + "\033[0m" + 
              "\033[33m" + "l" + "\033[0m" + 
              "\033[34m" + "d" + "\033[0m")
actions = ["Skip", "Reverse", "Draw two"]
wild_actions = ["Wild", "Draw four"]

# Create deck
deck = [NormalCard(color, num) for num in range(0, 10) for color in colors]
for i in range(1): deck += [NormalCard(color, num) for num in range(1, 10) for color in colors]
for i in range(2): deck += [ActionCard(color, action) for action in actions for color in colors]
for i in range(4): deck += [ActionCard(wild_color, wild_action) for wild_action in wild_actions]
deck += deck[:]

shuffle(deck)

game = Game(deck)

game.create_pile()

result = None

direction = 1

def clear_screen(name):
    if name == "nt": result = system("cls")
    else: result = system("clear")

def countdown(name):
    if name == "nt":
        while msvcrt.kbhit():
            msvcrt.getwch()
    else:
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
    for i in reversed(range(1, 6)):
        print("Switching to next player in {0}...".format(str(i)), end="\r")
        sleep(1)

def return_next_turn(turn, direction, game):
    if turn + direction > len(game.players) - 1:
        turn = 0
    elif turn + direction < 0:
        turn = len(game.players) - 1
    else:
        turn += direction
    return turn

def display_enter_message(next_turn, direction, game):
    enter_message = "Press Enter to end turn\n"
    if type(game.players[next_turn]) == AIPlayer:
        enter_message = "Press Enter to end turn (Next player is an AI)\n"
    input(enter_message)

clear_screen(name)

try:
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
            prin("The number you entered ({0}) is too big.\n".format(human_player_count))
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
        if not len(game.deck):
            print("No more cards left in the deck. Shuffling pile...")
            game.pile.shuffle()
            game.deck = game.pile[1:]
            del game.pile[1:]

        plr = game.players[turn]
        top_card = game.pile[0]

        if plr.uno_calls == 1:
            print("A player has called out UNO!")
            plr.uno_calls = 0
        if plr.uno_calls > 1:
            print("{0} players have called out UNO!")
            plr.uno_calls = 0

        if type(top_card) == ActionCard:
            formatted_top_card = format_card(top_card)
            if top_card.action == "Reverse":
                if len(game.players) == 2 and top_card.used == False:
                    if type(plr) == HumanPlayer:
                        print("Since this is a two player game and a {0} was used against you, you have been skipped...".format(formatted_top_card))

                    countdown(name)
                    turn = return_next_turn(turn, direction, game)
                    top_card.used = True

                    if name == "nt": result = system("cls")
                    else: result == system("clear")
                    continue
                if len(game.players) != 2:
                    print("A {0} was used so you are next!".format(format_card(top_card)))

            if top_card.used == False:
                if top_card.action == "Skip":
                    if type(plr) == HumanPlayer: print("You have been skipped by a {0}!".format(formatted_top_card))
                    countdown(name)
                    turn = return_next_turn(turn, direction, game)
                    top_card.used = True

                    if name == "nt": result = system("cls")
                    else: result == system("clear")
                    continue

                if top_card.action == "Draw two":
                    plr.draw_cards(2, game)
                    if type(plr) == HumanPlayer:
                        print("Oops! You have to draw two cards thanks to a {0}".format(formatted_top_card))
                        print("You drew the cards {0}".format(", ".join([format_card(card) for card in plr.hand[-2:]])))
                    else: print("Okay, I think I got some nice cards...")

                    display_enter_message(turn, direction, game)
                    countdown(name)
                    turn = return_next_turn(turn, direction, game)
                    top_card.used = True

                    if name == "nt": result = system("cls")
                    else: result == system("clear")
                    continue

                if top_card.action == "Draw four":
                    plr.draw_cards(4, game)
                    if type(plr) == HumanPlayer:
                        print("Ouch! You gotta draw four cards thanks to a {0}".format(formatted_top_card))
                        print("You drew the cards {0}".format(", ".join([format_card(card) for card in plr.hand[-4:]])))
                    else:
                        print("Okay...")
                    display_enter_message(turn, direction, game)
                    countdown(name)
                    turn = return_next_turn(turn, direction, game)
                    top_card.used = True

                    if name == "nt": result = system("cls")
                    else: result == system("clear")
                    continue

        print("-" * 75)
        print("TOP CARD:")
        print("-" * 75)
        print(format_card(top_card))
        if top_card.color == wild_color:
            print("Selected color: {0}".format(game.declared_color))

        plr.play(game)
        top_card = game.pile[0]

        if not plr.hand:
            if type(plr) == HumanPlayer: print("Congratulations! You won! 🎉🎉")
            else: print("I won! Woohoo! 🎉🎉")
            sys.exit()
        print("-" * 75)
        print("PILE:")
        print("-" * 75)
        for card in game.pile:
            print(format_card(card))

        if type(plr) == AIPlayer:
            print("-" * 75)

        else:
            print("-" * 75)
            print("HAND:")
            print("-" * 75)
            for card in plr.hand:
                print(format_card(card))
            print("-" * 75)

        if type(top_card) == ActionCard:
            if top_card.action == "Reverse":
                direction *= -1
        print(direction)
        print(turn)
        turn = return_next_turn(turn, direction, game)
        display_enter_message(turn, direction, game)
        countdown(name)
        if name == "nt": result = system("cls")
        else: result == system("clear")

except KeyboardInterrupt:
    print("\nGoodbye!")

