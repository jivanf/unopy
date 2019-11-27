import re
from action_card import ActionCard
from normal_card import NormalCard
import functions
import sys

class Player():
    def __init__(self, game):
        self.hand = list()
        self.game = game

    def __non_integer_input_message(self, count):
        return {
            1: "Uh oh, that's not a number! Please try again:\n",
            2: "Please enter the number that represents the card. The list is above.\n",
            3: "Ok, this is not funny. Just do as I say and we can keep playing.\n",
            4: "Last chance. Enter a number.\n",
        }[count]

    # TODO: Add funny messages
    def __invalid_integer_input_message(self, count):
        return {
            1: "The number you selected is not within the range of your hand size.\n",
            2: "You need to select a number from the list, or else we can't keep playing.\n",
            3: "Please select a valid number.",
            4: "Last chance. Enter a valid number\n",
        }[count]

    def __card_cant_be_placed_message(self, count):
        return {
            1: "The card you selected can't be placed. Please try placing another card.\n",
            2: "You can't place this card!\n",
            3: self.__return_card_suggestions(),
            4: "Last chance. Enter a valid card or draw one from the deck.\n",
        }[count]

    def __return_card_suggestions(self):
        possible_cards = [x for x in self.hand if functions.check_if_card_can_be_placed(x, self.game.pile[0])] 
        if not possible_cards:
            return "You can't place any cards. Try drawing...\n"
        else:
            if len(possible_cards) == 1:
                return "Psst... Try placing a {0}\n".format(functions.format_card(possible_cards[0]))
            else:
                possible_cards = [functions.format_card(x) for x in possible_cards]
                possible_cards[-1] = "or a " + possible_cards[-1]
                return "Psst... Try placing a {0}\n".format(", ".join(possible_cards))

    def draw_cards(self, amount):
        self.hand += self.game.deck[:amount]
        del self.game.deck[:amount]

    def play(self):
        print("-" * 75)
        print("AVAILABLE CARDS")
        print("-" * 75)

        for i, card in enumerate(self.hand): print("{0}) {1}".format(str(i + 1), functions.format_card(card)))
        non_integer_count = 0
        invalid_integer_count = 0
        card_cant_be_placed_count = 0
        toggle = 0
        choice = None
        while True:
            if 5 in (non_integer_count, invalid_integer_count, card_cant_be_placed_count): 
                print("ok")
                sys.exit()
            if toggle == 0: choice = input("Choose a card to place (enter the number of the card):\n")
            elif toggle == 1: choice = input(self.__non_integer_input_message(non_integer_count))
            elif toggle == 2: choice = input(self.__invalid_integer_input_message(invalid_integer_count))
            elif toggle == 3: choice = input(self.__card_cant_be_placed_message(card_cant_be_placed_count))
            else: choice == input(self.__invalid_integer_input_message(invalid_integer_count))


            try:
                choice = int(choice) - 1
            except ValueError:
                non_integer_count += 1
                toggle = 1
                continue

            if not 0 <= choice < len(self.hand):
                invalid_integer_count += 1
                toggle = 2
                continue
            card = self.hand[choice]
            if functions.check_if_card_can_be_placed(card, self.game.pile[0], self.game.declared_color):
                self.game.pile.insert(0, self.hand.pop(choice))
                break
            else:
                card_cant_be_placed_count += 1
                toggle = 3
