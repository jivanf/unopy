import random
from game import Game
from player import Player
from action_card import ActionCard
from normal_card import NormalCard
from functions import format_card

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

plr = Player(game)
plr.draw_cards(7)
print("-" * 75)
print("TOP CARD:")
print("-" * 75)
print(format_card(game.pile[-1]))

print("-" * 75)
print("CURRENT HAND:")
print("-" * 75)
for card in plr.hand:
    print(format_card(card))

print("-" * 75)
print("TEST:")
print("-" * 75)
for card in plr.hand:
    print(format_card(card))
    plr.place_card(card) 
