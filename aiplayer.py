from player import Player
import functions

class AIPlayer(Player):
    def __init__(self, game):
        Player.__init__(self, game)

    def play(self):
        for card in self.hand:
            check = functions.check_if_card_can_be_placed(card, self.game.pile[0], self.game.declared_color)
            if check:
                self.game.pile.insert(0, self.hand.pop(self.hand.index(card)))
                print("I can place a {0}!".format(functions.format_card(card)))
                break
            print("I can't place a {0} <:(".format(functions.format_card(card)))
