from action_card import ActionCard
from functions import format_card

class Game():
    def __init__(self, deck):
        self.deck = deck
        # When using a wild card, this variable will store the color decided by the player
        self.declared_color = None

    def create_pile(self):
        self.pile = list()
        top_card = self.deck[0]
        if type(top_card) == ActionCard or top_card.color == "Wild":
            print("Unable to put card '{0}' on pile. Returning card and redrawing...".format(format_card(top_card)))
            self.deck += [self.deck.pop(0)]
            self.create_pile()
        else:
            self.pile.append(top_card)
