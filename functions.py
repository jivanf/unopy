from normal_card import NormalCard
from action_card import ActionCard
import re

def format_card(card):
    if type(card) == NormalCard:
        return "{0} {1}".format(card.color, card.number)
    else:
        return "{0} {1}".format(card.color, card.action)

# declared_color hasn't been implemented yet so its default value is None
def check_if_card_can_be_placed(card_to_place, card_placed, declared_color=None):
    card_to_place_color_text = re.sub(r"\x1b\[[0-9]+m", "", card_to_place.color)
    card_placed_color_text = re.sub(r"\x1b\[[0-9]+m", "", card_placed.color)
    
    # TODO: Change "or" condition to "and" after allowing users to select a color after placing a wild
    if card_to_place_color_text == "Wild" or card_to_place_color_text == declared_color:
        return True

    if card_placed_color_text == "Wild":
        return True

    # Change "or" condition to "and" after allowing users to select a color after placing a wild
    if card_to_place_color_text == card_placed_color_text or card_to_place_color_text == declared_color:
        return True

    # TODO: Check if an ActionCard can be placed
    if type(card_to_place) == ActionCard:
        if type(card_placed) == ActionCard:
            if card_to_place.action == card_placed.action:
                return True

    # Check if a NormalCard can be placed
    if type(card_to_place) == NormalCard:
        if type(card_placed) == NormalCard:
            if card_to_place.number == card_placed.number:
                        return True
    return False
