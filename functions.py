from normal_card import NormalCard
def format_card(card):
    if type(card) == NormalCard:
        return "{0} {1}".format(card.color, card.number)
    else:
        return "{0} {1}".format(card.color, card.action)
