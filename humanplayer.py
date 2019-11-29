import re
import functions
import sys
from action_card import ActionCard
from normal_card import NormalCard
from player import Player

class HumanPlayer(Player):
    def __init__(self):
        Player.__init__(self)

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
            3: "Please select a valid number.\n",
            4: "Last chance. Enter a valid number\n",
        }[count]

    def __card_cant_be_placed_message(self, count, game):
        return {
            1: "The card you selected can't be placed. Please try placing another card.\n",
            2: "You can't place this card!\n",
            3: self.__return_card_suggestions(game),
            4: "Last chance. Enter a valid card or draw one from the deck.\n",
        }[count]

    def __return_card_suggestions(self, game):
        possible_cards = [x for x in self.hand if functions.check_if_card_can_be_placed(x, game.pile[0])] 
        if not possible_cards:
            return "You can't place any cards. Try drawing...\n"
        else:
            if len(possible_cards) == 1:
                return "Psst... Try placing a {0}\n".format(functions.format_card(possible_cards[0]))
            else:
                possible_cards = [functions.format_card(x) for x in possible_cards]
                possible_cards[-1] = "or a " + possible_cards[-1]
                return "Psst... Try placing a {0}\n".format(", ".join(possible_cards))

    def play(self, game):
        try:
            print("-" * 75)
            print("AVAILABLE CARDS")
            print("-" * 75)

            for i, card in enumerate(self.hand): print("{0}) {1}".format(str(i + 1), functions.format_card(card)))
            print("-" * 75)
            non_integer_count = 0
            invalid_integer_count = 0
            card_cant_be_placed_count = 0
            toggle = 0
            choice = None
            while True:
                if 5 in (non_integer_count, invalid_integer_count, card_cant_be_placed_count): 
                    print("ok")
                    sys.exit()
                if toggle == 0: choice = input("Choose a card to place (enter the number of the card) or type 'D' to draw a card:\n")
                elif toggle == 1: choice = input(self.__non_integer_input_message(non_integer_count))
                elif toggle == 2: choice = input(self.__invalid_integer_input_message(invalid_integer_count))
                elif toggle == 3: choice = input(self.__card_cant_be_placed_message(card_cant_be_placed_count, game))
                else: choice == input(self.__invalid_integer_input_message(invalid_integer_count))

                if choice.lower() == "d":
                    self.draw_cards(1, game)
                    drawn_card = self.hand[-1]
                    print("-" * 75)
                    if functions.check_if_card_can_be_placed(drawn_card, game.pile[0], game.declared_color):
                        place_card = input("You drew a {0} and you can place it or keep it. Do you want to place it? (y/n)\n".format(functions.format_card(drawn_card)))
                        if place_card.lower() == "y":
                            game.pile.insert(0, self.hand.pop(-1))
                        return
                    else:
                        print("You drew a {0} but you can't place it".format(functions.format_card(drawn_card)))
                        break
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
                if functions.check_if_card_can_be_placed(card, game.pile[0], game.declared_color):
                    game.pile.insert(0, self.hand.pop(choice))
                    break
                else:
                    card_cant_be_placed_count += 1
                    toggle = 3
        except KeyboardInterrupt:
            print("\nGoodbye!")
            sys.exit()
