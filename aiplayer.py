from player import Player
import functions
from random import randint
from collections import Counter

class AIPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)

    def play(self, game):
        wild_color = ("\033[31m" + "W" + "\033[0m" + 
                      "\033[32m" + "i" + "\033[0m" + 
                      "\033[33m" + "l" + "\033[0m" + 
                      "\033[34m" + "d" + "\033[0m")

        for card in self.hand:
            check = functions.check_if_card_can_be_placed(card, game.pile[0], game.declared_color)

            if check:
                if len(self.hand) == 2:
                    uno_call_chance = randint(0, 10)
                    if uno_call_chance < 8:
                        print("UNO!")
                        for player in game.players:
                            if player == self:
                                continue

                            else:
                                player.uno_calls.append(self.name) 

                    else:
                        print("Oops! I forgot to call out UNO...")
                        self.draw_cards(2, game)

                game.pile.insert(0, self.hand.pop(self.hand.index(card)))

                if card.color == wild_color:
                    hand_colors = [card.color for card in self.hand]
                    max_color = Counter(hand_colors).most_common(1)[0][0]

                    if max_color == wild_color:
                        max_color = Counter(hand_colors).most_common(2)[1][0]

                    game.declared_color = max_color

                    print("I'm placing a {0} and I'm gonna choose the color {1}".format(functions.format_card(card), max_color))
                    return

                print("I'm placing a {0}".format(functions.format_card(card)))
                return

        print("I can't place any cards, I'm gonna draw one...")
        self.draw_cards(1, game)

        drawn_card = self.hand[-1]

        if functions.check_if_card_can_be_placed(drawn_card, game.pile[0], game.declared_color):
            print("Yes! Got a {0}".format(functions.format_card(drawn_card)))
            game.pile.insert(0, self.hand.pop(-1))
            if drawn_card.color == wild_color:
                hand_colors = [card.color for card in self.hand]
                max_color = Counter(hand_colors).most_common(1)[0][0]
                game.declared_color = max_color

                print("I'm gonna choose the color {0}".format(max_color))

        else:
            print("I can't place the card that I got...")
