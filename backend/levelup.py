import logging
from essentials import Deck, wait

REJECT = -1
ACK = 0
BOTTOM = 1
DRAW = 2
PLAY = 3
SCORE = 4
LEVEL = 5
COLOR = 6
END = 7

deal_wait_time = .2
wait_time = .5

class Game:
    def __init__(self, table, dealer, dealer_level):
        self.table = table
        self.dealer = dealer
        self.level = dealer_level
        self.color = None

        self.deck = Deck()
        self.deck.shuffle()

        self.bottom = []
        self.cards = [[], [], [], []]
        
        self.round_cards = []
        self.round_winner = dealer
        self.current_player = dealer

        self.score = 0
        self.round_score = 0

    def game_play(self):
        self.announce_level()
        self.deal_cards()
        wait(wait_time, self.has_declared, self.default_declare)

        self.add_bottom_to_dealer()
        logging.info("Initial cards:")
        self.debug_show_cards()
        wait(wait_time, self.dealer_selected_bottom, self.default_select_bottom)

        cnt = 1
        while len(self.cards[self.round_winner]):
            logging.info("---------------")
            logging.info("Round " + str(cnt) + ".")

            self.debug_show_cards()
            self.round_cards = [None, None, None, None]

            self.current_player = self.round_winner
            self.announce_player_play()
            wait(wait_time, self.player_played, self.default_player_play)

            self.current_player = (self.current_player + 1) % 4
            self.announce_player_play()
            wait(wait_time, self.player_played, self.default_player_play)

            self.current_player = (self.current_player + 1) % 4
            self.announce_player_play()
            wait(wait_time, self.player_played, self.default_player_play)

            self.current_player = (self.current_player + 1) % 4
            self.announce_player_play()
            wait(wait_time, self.player_played, self.default_player_play)

            self.current_player = (self.current_player + 1) % 4
            self.announce_player_play()

            self.debug_show_round_cards()

            self.judge_round()
            self.announce_round_winner()

            wait(1, None, None)
            cnt += 1
        
        logging.info("---------------")
        self.bottom_scoring()
        self.announce_final_score()
        return self.score, self.is_dealer_team(self.round_winner)

    def announce_level(self):
        self.announce({
            'verb': LEVEL,
            'level': self.level
        })

    def deal_cards(self):
        t = self.dealer
        for i in range(48):
            self.deal_card_to_player(t, self.deck.order[i])
            wait(deal_wait_time, None, None)
            t = (t + 1) % 4

    def deal_card_to_player(self, player, card_id):
        self.cards[player].append(card_id)
        for i in range(4):
            if i == player:
                self.tell(i, {
                    'verb': DRAW,
                    'player': player,
                    'card': card_id
                })
            else:
                self.tell(i, {
                    'verb': DRAW,
                    'player': player
                })

    def declare(self, player, card_id):
        if card_id not in self.cards[player]:
            self.tell(player, {'verb': REJECT})
            return

        card = self.deck.card(card_id)
        if self.level == card[1]:
            self.color = card[0]
        self.anounce_main_color()

    def default_declare(self):
        id = self.deck.order[50]
        if id == 53 or id == 52:
            id = self.deck.order[51]
        if id == 53 or id == 52:
            id = self.deck.order[52]
        card = self.deck.card(id)
        self.color = card[0]
        self.announce_main_color()

    def has_declared(self):
        return self.color != None

    def announce_main_color(self):
        self.announce({
            'verb': COLOR,
            'color': self.color
        })

    def add_bottom_to_dealer(self):
        self.cards[self.dealer].extend(self.deck.order[48:54])
        self.tell(self.dealer, {
            'verb': BOTTOM,
            'cards': self.deck.order[48:54]
        })

    def dealer_selected_bottom(self):
        return self.bottom != []
    
    def dealer_select_bottom(self, player, bottom):
        if player != self.dealer:
            self.tell(player, {'verb': REJECT})
            return
        if len(bottom) != 6:
            self.tell(player, {'verb': REJECT})
            return
        for i in bottom:
            if i not in self.cards[self.dealer]:
                self.tell(player, {'verb': REJECT})
                return
        self.bottom = bottom
        for i in bottom:
            self.cards[self.dealer].remove(i)
        self.tell(player, {'verb': ACK, 'bottom': self.bottom})

    def default_select_bottom(self):
        self.dealer_select_bottom(self.dealer, self.choose_least_cards(self.dealer, 6, None))

    def announce_player_play(self):
        self.announce({
            'verb': PLAY,
            'round_cards': self.round_cards,
            'current_player': self.current_player
        })

    def player_play(self, player, cards):
        if player != self.current_player:
            self.tell(player, {'verb': REJECT})
            return
        if any([card not in self.cards[player] for card in cards]):
            self.tell(player, {'verb': REJECT})
            return
        if len(cards) == 0:
            self.tell(player, {'verb': REJECT})
            return
        if player == self.round_winner:
            # first play in a round
            if len(cards) > 1:
                if any([self.is_main_card(card) for card in cards]):
                    self.tell(player, {'verb': REJECT})
                    return
                colors = set([self.deck.color(card) for card in cards])
                if len(colors) != 1:
                    self.tell(player, {'verb': REJECT})
                    return
        else:
            # follow
            required = len(self.round_cards[self.round_winner])
            mark = self.round_cards[self.round_winner][0]
            if len(cards) != required:
                self.tell(player, {'verb': REJECT})
            played = self.cards_of_color(cards, mark)
            owned = self.cards_of_color(self.cards[player], mark)
            if len(played) < required and len(played) < len(owned):
                self.tell(player, {'verb': REJECT})
                return
        self.round_cards[player] = cards
        for i in cards:
            self.cards[player].remove(i)

    def default_player_play(self):
        if self.current_player == self.round_winner:
            self.player_play(self.current_player, self.choose_least_cards(self.current_player, 1, None))
        else:
            self.player_play(self.current_player, self.choose_least_cards(self.current_player, len(self.round_cards[self.round_winner]), self.round_cards[self.round_winner][0]))

    def player_played(self):
        return self.round_cards[self.current_player] != None

    def judge_round(self):
        res = self.round_winner
        for i in range(1, 4):
            t = (self.round_winner + i) % 4
            if self.less(self.round_cards[res], self.round_cards[t]):
                res = t
        
        self.round_winner = res

        score = 0
        if not self.is_dealer_team(res):
            for i in range(4):
                for j in self.round_cards[i]:
                    if self.deck.card(j)[1] == '5':
                        score += 5
                    elif self.deck.card(j)[1] == '10':
                        score += 10
                    elif self.deck.card(j)[1] == 'K':
                        score += 10

        self.round_score = score
        self.score += score

    def announce_round_winner(self):
        self.announce({
            'verb': SCORE,
            'winner': self.round_winner,
            'round_score': self.round_score,
            'total_score': self.score
        })

    def bottom_scoring(self):
        score = 0
        if not self.is_dealer_team(self.round_winner):
            for j in self.bottom:
                if self.deck.card(j)[1] == '5':
                    score += 5
                elif self.deck.card(j)[1] == '10':
                    score += 10
                elif self.deck.card(j)[1] == 'K':
                    score += 10

        self.round_score = score
        self.score += score * 2

    def announce_final_score(self):
        self.announce({
            'verb': SCORE,
            'winner': self.round_winner,
            'round_score': self.round_score,
            'total_score': self.score
        })

    def announce(self, obj):
        self.announce_callback(self.table, obj)

    def tell(self, player, obj):
        self.tell_callback(self.table, player, obj)

    def is_main_card(self, card_id):
        card = self.deck.card(card_id)
        if self.color == card[0]:
            return True
        if 'JOKER' == card[1] or '2' == card[1] or self.level == card[1]:
            return True
        return False
    
    def cards_of_color(self, cards, card_id):
        res = []
        if self.is_main_card(card_id):
            for i in cards:
                if self.is_main_card(i):
                    res.append(i)
        else:
            for i in cards:
                if not self.is_main_card(i) and self.deck.card(card_id)[0] == self.deck.card(i)[0]:
                    res.append(i)
        return res

    def less(self, cards1, cards2):
        all_main_1 = all([self.is_main_card(card) for card in cards1])
        all_main_2 = all([self.is_main_card(card) for card in cards2])
        color = self.deck.card(cards1[0])[0]
        if all_main_1:
            if all_main_2:
                return self.value_of_cards(cards1) < self.value_of_cards(cards2)
            else:
                return False
        else:
            if all_main_2:
                return True
            elif any([self.deck.card(card)[0] != color for card in cards2]):
                return False
            else:
                return self.value_of_cards(cards1) < self.value_of_cards(cards2)

    def value_of_card(self, card):
        c = self.deck.card(card)
        if c[1] == 'JOKER':
            card += 100000
        elif c[1] == self.level:
            card += 10000
        elif c[1] == '2':
            card += 1000
        if c[0] == self.color:
            card += 100
        return card

    def value_of_cards(self, cards):
        return max([self.value_of_card(card) for card in cards])

    def is_dealer_team(self, player):
        return player == (self.dealer + 0) % 4 or player == (self.dealer + 2) % 4

    def choose_least_cards(self, player, number, card_for_color):
        res = []
        if card_for_color != None:
            coc = self.cards_of_color(self.cards[player], card_for_color)
            coc.sort(reverse = False, key = self.value_of_card)
            num = min(len(coc), number)
            res.extend(coc[0:num])
            number -= num
        if number:
            cards = [i for i in self.cards[player] if  i not in res]
            cards.sort(reverse = False, key = self.value_of_card)
            res.extend(cards[0:number])
        return res

    def debug_show_cards(self):
        for i in range(4):
            log = "Player " + str(i) + ": "
            t = self.cards[i]
            t.sort(reverse = True, key = self.value_of_card)
            for j in t:
                card = self.deck.card(j)
                log += card[0] + card[1] + ", "
            if i == self.dealer:
                logging.info(log + " [d]")
            else:
                logging.info(log)

    def debug_show_round_cards(self):
        for i in range(4):
            log = "Player " + str(i) + " played: "
            t = self.round_cards[i]
            t.sort(reverse = True, key = self.value_of_card)
            for j in t:
                card = self.deck.card(j)
                log += card[0] + card[1] + ", "
            if i == self.round_winner:
                logging.info(log + " [r]")
            else:
                logging.info(log)


class Match:
    pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    wait_time = 0
    deal_wait_time = 0
    g = Game(1, 0, '3')
    g.game_play()