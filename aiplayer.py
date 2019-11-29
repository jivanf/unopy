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
                print("-" * 75)
                print("I'm placing a {0}".format(functions.format_card(card)))
                print("-" * 75)
                return
        print("I can't place any cards, I'm gonna draw one...")
        self.draw_cards(1, game)
        drawn_card = self.hand[-1]
        if functions.check_if_card_can_be_placed(drawn_card, game.pile[0], game.declared_color):
            print("Yes! Got a {0}".format(functions.format_card(drawn_card)))
            game.pile.insert(0, self.hand.pop(-1))
        else:
            print("Got a {0} but I can't place it!".format(functions.format_card(drawn_card)))

