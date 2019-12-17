class Player():
    def __init__(self):
        self.hand = list()
        self.uno_calls = 0

    def draw_cards(self, amount, game):
        self.hand += game.deck[:amount]
        del game.deck[:amount]
