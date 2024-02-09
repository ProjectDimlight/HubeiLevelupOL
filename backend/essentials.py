import random
import time

def wait(seconds, cond, default_op):
    start_time = time.time()
    while time.time() - start_time < seconds:
        if cond and cond():
            break
        time.sleep(0.1)
    else:
        if default_op:
            default_op()

class Deck:
    def __init__(self):
        self.colors = ['♠', '♥', '♣', '♦']
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

    def card(self, id):
        return self.deck[id]

    def shuffle(self):
        random.shuffle(self.order)
        return self.order