from player import Player
import functions

class AIPlayer(Player):
    def __init__(self):
        Player.__init__(self)

    def play(self, game):
        for card in self.hand:
            check = functions.check_if_card_can_be_placed(card, game.pile[0], game.declared_color)
            if check:
                game.pile.insert(0, self.hand.pop(self.hand.index(card)))
                print("I'm placing a {0}".format(functions.format_card(card)))
                return
        print("I can't place any cards, I'm gonna draw...")
