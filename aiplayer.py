from action_card import ActionCard
from normal_card import NormalCard
from player import Player
import re
from functions import format_card

class AIPlayer(Player):
    def __init__(self, game):
        Player.__init__(self, game)

    def play(self):
        for card in self.hand:
            top_card = self.game.pile[-1]
            
            # Remove ANSI codes for comparison 
            top_card_color_text = re.sub(r"\x1b\[[0-9]+m", "", top_card.color)
            current_card_color_text = re.sub(r"\x1b\[[0-9]+m", "", card.color)

            if current_card_color_text == "Wild" and current_card_color_text == self.game.declared_color:
                print("I can place the card {0}!".format(format_card(card)))
                self.game.pile.append(self.hand.pop(self.hand.index(card)))
                return True

            if top_card_color_text == "Wild":
                print("I can place the card {0}!".format(format_card(card)))
                self.game.pile.append(self.hand.pop(self.hand.index(card)))
                return True

            if current_card_color_text == top_card_color_text or current_card_color_text == self.game.declared_color:
                print("I can place the card {0}!".format(format_card(card)))
                self.game.pile.append(self.hand.pop(self.hand.index(card)))
                return True

            # Check if an ActionCard can be placed
            if type(card) == ActionCard:
                if type(top_card) == ActionCard:
                    if card.action == top_card.action:
                        print("I can place the card {0}!".format(format_card(card)))
                        self.game.pile.append(self.hand.pop(self.hand.index(card)))
                        return True

            # Check if a NormalCard can be placed
            if type(card) == NormalCard:
                if type(top_card) == NormalCard:
                    if card.number == top_card.number:
                        print("I can place the card {0}!".format(format_card(card)))
                        self.game.pile.append(self.hand.pop(self.hand.index(card)))
                        return True
            print("Go draw a card")
            return False


            
