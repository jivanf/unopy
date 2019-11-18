import re
from action_card import ActionCard
from normal_card import NormalCard

class Player():
    def __init__(self):
        self.hand = list()

    def draw_cards(self, game, amount):
        self.hand += game.deck[:amount]

    def place_card(self, card, game):
        top_card = game.pile[-1]
        
        # Remove ANSI codes for comparison 
        top_card_color_text = re.sub(r"\x1b\[[0-9]+m", "", top_card.color)
        current_card_color_text = re.sub(r"\x1b\[[0-9]+m", "", card.color)

        if current_card_color_text == "Wild":
            print("You can place this card!")
            return True

        if top_card_color_text == "Wild":
            print("You can place this card!")
            return True

        if current_card_color_text == top_card_color_text or current_card_color_text == game.declared_color:
            print("You can place this card!")
            return True

        # Check if an ActionCard can be placed
        if type(card) == ActionCard:
            if type(top_card) == ActionCard:
                if card.action == top_card.action:
                    print("You can place this card!")
                    return True

        # Check if a NormalCard can be placed
        if type(card) == NormalCard:
            if type(top_card) == NormalCard:
                if card.number == top_card.number:
                    print("You can place this card!")
                    return True
        print("Go draw a card")
        return False
