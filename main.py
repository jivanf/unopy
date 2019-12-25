from random import shuffle
from game import Game
from humanplayer import HumanPlayer
from bot_player import BotPlayer
from action_card import ActionCard
from normal_card import NormalCard
from functions import format_card
from os import system, name, get_terminal_size
from time import sleep
from copy import deepcopy
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
deck += deepcopy(deck)

shuffle(deck)

game = Game(deck)
game.create_pile()

result = None

direction = 1

def clear_screen():
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
    next_player = game.players[next_turn]
    input("Press Enter to end turn (Next player is {0})\n".format(next_player.name))

def display_player_order(game, direction):
    terminal_size = get_terminal_size()
    players = game.players
    message_buffer = ""
    message = ""
    selected_arrow = "->" if direction == 1 else "<-"
    print("\n" * ((terminal_size.lines - 1) // 2), "PLAYER ORDER".center(terminal_size.columns - 1))
    
    for player in players:
        if players[-1] == player:
            message_buffer += player.name
        else:
            message_buffer += player.name + " {0} ".format(selected_arrow)

    for char in message_buffer:
        message += char
        print(message.center(terminal_size.columns - 1), end="\r")
        sleep(0.1)
    sleep(5)

clear_screen()

try:
    while True:
        human_player_count = None

        try:
            human_player_count = int(input("How many people are going to play? (Up to 10 players, including bots)\n"))

        except ValueError:
            print("{0} is not a number...\n".format(human_player_count))
            continue
        
        if human_player_count < 0:
            print("The number you entered ({0}) is a negative number. I can't use those.\n".format(human_player_count))
            continue

        if human_player_count > 10:
            print("The number you entered ({0}) is too big.\n".format(human_player_count))
            continue

        ai_player_count = None 

        try:
            ai_player_count = int(input("How many bots do you want? (Up to 10 players, including human players)\n"))

        except ValueError:
            print("{0} is not a number...\n".format(ai_player_count))
            continue

        if human_player_count + ai_player_count > 10:
            print("The amount of human players and bots is too big.\n")
            continue

        if ai_player_count < 0:
            print("The number you entered ({0}) is a negative number. I can't use those.\n".format(human_player_count))
            continue

        elif human_player_count + ai_player_count == 0:
            print("Do you really want to start a game with 0 players? I don't think so.\n")
            continue

        elif human_player_count + ai_player_count == 1:
            print("The game can't start with only one player!")
            continue

        for i in range(0, ai_player_count):
            bot_name = "Bot{0}".format(i + 1)
            bot_player = BotPlayer(bot_name)
            bot_player.draw_cards(7, game)
            game.add_player(bot_player)

        for i in range(0, human_player_count):
            human_player = None
            player_name = input("Player {0}'s name? Default is Player{0}: ".format(i + 1))
            
            if player_name in [player.name for player in game.players]:
                while True:
                    player_name = input("That name is already being used. Please use a different name: ")
                    if player_name in [player.name for player in game.players]:
                        continue
                    break

            if not player_name:
                default_name = "Player{0}".format(i + 1)
                human_player = HumanPlayer(default_name)

            else:
                human_player = HumanPlayer(player_name)

            human_player.draw_cards(7, game)
            game.add_player(human_player)
        break

    turn = 0

    shuffle(game.players)
    clear_screen()
    display_player_order(game, direction)
    clear_screen()

    while True:
        if not len(game.deck):
            print("No more cards left in the deck. Shuffling pile...")
            game.pile.shuffle()
            game.deck = game.pile[1:]
            del game.pile[1:]

        player = game.players[turn]
        top_card = game.pile[0]

        if len(player.uno_calls) == 1:
            print("{0} has called out UNO!".format(player.uno_calls[0]))
            player.uno_calls = list()

        if len(player.uno_calls) > 1:
            message = ""
            for uno_player in player.uno_calls:
                if player.uno_calls[-2] == uno_player:
                    message += "{0} and {1}".format(uno_player, player.uno_calls[-1])
                    break
                message += "{0}, ".format(uno_player)
            message += " have called out UNO!"
            
            print(message)

        if type(top_card) == ActionCard:
            formatted_top_card = format_card(top_card)
            if top_card.used == False:
                if top_card.action == "Reverse":
                    if len(game.players) == 2:
                        if type(player) == HumanPlayer: print(("Since this is a two player game and a "
                                                            "{0} was used against you, " 
                                                            "you have been skipped...").format(formatted_top_card))

                        else: print("Looks like I got skipped")

                        turn = return_next_turn(turn, direction, game)
                        display_enter_message(turn, direction, game)
                        countdown(name)
                        clear_screen()

                    if len(game.players) != 2:
                        print("another test")
                        clear_screen()
                        display_player_order(game, direction)
                        clear_screen()
                        print("A {0} was used so you are next!".format(format_card(top_card)))

                if top_card.action == "Skip":
                    if type(player) == HumanPlayer: print("You have been skipped by a {0}!".format(formatted_top_card))
                    else: print("I got skipped...")

                    turn = return_next_turn(turn, direction, game)
                    display_enter_message(turn, direction, game)
                    countdown(name)
                    clear_screen()


                if top_card.action == "Draw two":
                    player.draw_cards(2, game)
                    if type(player) == HumanPlayer:
                        print("Oops! You have to draw two cards thanks to a {0}".format(formatted_top_card))
                        print("You drew the cards {0}".format(", ".join([format_card(card) for card in player.hand[-2:]])))

                    else: print("Okay, I think I got some nice cards...")

                    turn = return_next_turn(turn, direction, game)
                    display_enter_message(turn, direction, game)
                    countdown(name)
                    clear_screen()
                    

                if top_card.action == "Draw four":
                    player.draw_cards(4, game)
                    if type(player) == HumanPlayer:
                        print("Ouch! You gotta draw four cards thanks to a {0}".format(formatted_top_card))
                        print("You drew the cards {0}".format(", ".join([format_card(card) for card in player.hand[-4:]])))

                    else:
                        print("Okay...")

                    turn = return_next_turn(turn, direction, game)
                    display_enter_message(turn, direction, game)
                    countdown(name)
                    clear_screen()

                top_card.used = True
                continue

        print("-" * 60)
        print("TOP CARD:")
        print("-" * 60)
        print(format_card(top_card))
        if top_card.color == wild_color:
            print("Selected color: {0}".format(game.declared_color))

        player.play(game)
        top_card = game.pile[0]

        if not player.hand:
            if type(player) == HumanPlayer: print("Congratulations! You won! 🎉🎉")
            else: print("I won! Woohoo! 🎉🎉")
            sys.exit()

        print("-" * 60)
        print("PILE:" if len(game.pile) < 20 else "PILE (TOP 20 CARDS):")
        print("-" * 60)
        for card in game.pile[:20]:
            print(format_card(card))

        if type(player) == BotPlayer:
            print("-" * 60)

        else:
            print("-" * 60)
            print("HAND:")
            print("-" * 60)
            for card in player.hand:
                print(format_card(card))
            print("-" * 60)

        if type(top_card) == ActionCard:
            if top_card.action == "Reverse" and top_card.used == False:
                direction *= -1

        turn = return_next_turn(turn, direction, game)
        display_enter_message(turn, direction, game)
        countdown(name)
        clear_screen()

except KeyboardInterrupt:
    print("\nGoodbye!")
