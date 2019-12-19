class Player():
    def __init__(self, name):
        self.hand = list()
        # TODO: change uno_calls to set
        self.uno_calls = list()
        self.name = name

    def draw_cards(self, amount, game):
        self.hand += game.deck[:amount]
        del game.deck[:amount]
