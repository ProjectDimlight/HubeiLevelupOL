import random

class Deck:
    def __init__():
        self.colors = ['♠', '♥', '♣', '♦️']
        self.levels = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
        self.jokers = [('b', 'JOKER'), ('r', 'JOKER')]
        self.deck = []
        for i in self.colors:
            for j in self.levels:
                self.deck.append((i, j))
        for i in self.jokers:
            self.deck.append(i)
        self.order = []
        for i in range(54):
            self.order.append(i)

    def card(id):
        return self.deck[id]

    def shuffle():
        random.shuffle(self.order)
        return self.order