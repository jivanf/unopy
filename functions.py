from normal_card import NormalCard
from action_card import ActionCard
import re

def format_card(card):
    if type(card) == NormalCard:
        return "{0} {1}".format(card.color, card.number)
    else:
        return "{0} {1}".format(card.color, card.action)

def remove_ansii_code(color):
    return re.sub(r"\x1b\[[0-9]+m", "", color)

def check_if_card_can_be_placed(card_to_place, card_placed, declared_color):
    card_to_place_color_text = remove_ansii_code(card_to_place.color) 
    card_placed_color_text = remove_ansii_code(card_placed.color) 
    declared_color_text = None
    if declared_color is not None: declared_color_text = remove_ansii_code(declared_color)
    
    if card_to_place_color_text == "Wild":
        return True

    if card_placed_color_text == "Wild" and declared_color_text == card_to_place_color_text:
        return True

    if card_to_place_color_text == card_placed_color_text:
        return True

    # Check if an ActionCard can be placed
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
