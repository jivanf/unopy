class Player():
    def __init__(self):
        self.hand = list()

    def draw_cards(self, amount, game):
        self.hand += game.deck[:amount]
        del game.deck[:amount]

