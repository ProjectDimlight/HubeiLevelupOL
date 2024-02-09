import time

REJECT = -1
ACK = 0
BOTTOM = 1
DRAW = 2
PLAY = 3
SCORE = 4
LEVEL = 5
COLOR = 6
END = 7

wait_time = 2

class Game:
    def __init__(self, dealer, dealer_level, deck):
        self.dealer = dealer
        self.level = banker_level
        self.deck = deck

        self.bottom = []
        self.cards = [[], [], [], []]
        
        self.round_cards = []
        self.round_winner = dealer
        self.current_player = dealer

        self.score = 0
        self.round_score = 0

    def wait(self, seconds, cond, default_op):
        start_time = time.time()
        while time.time() - start_time < seconds:
            if cond():
                break
            time.sleep(0.1)
        else:
            default_op()

    def game_play(self):
        self.announce_level()
        deal_cards()
        wait(wait_time, self.has_declared, self.default_declare)
        self.announce_main_color()

        self.add_bottom_to_dealer()
        wait(wait_time, self.dealer_selected_bottom, self.default_select_bottom)

        while len(self.cards[self.round_winner]):
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

            self.current_player = -1
            self.announce_player_play()

            self.judge_round()
            self.announce_round_winner()
        
        self.bottom_scoring()
        self.announce_final_score()
        return self.score, self.is_dealer_team(self.round_winner)

    def announce_level(self):
        self.announce({
            verb: LEVEL,
            level: self.level
        })

    def deal_cards(self):
        t = dealer
        for i in range(48):
            self.deal_card_to_player(t, self.deck.order[i])
            wait(1, None, None)
            t = (t + 1) % 4

    def deal_card_to_player(self, player, card_id):
        self.cards[player].append(card_id)
        self.tell(player, {
            verb: CARD,
            card: card_id
        })

    def declare(self, player, card_id):
        if card_id not in self.cards[player]:
            self.tell(player, {verb: REJECT})
            return

        card = self.deck.card(card_id)
        if self.level == card[1]:
            self.color = card[0]
        self.anounce_main_color()

    def default_declare(self):
        card = self.deck.card(50)
        self.color = card[0]
        self.announce_main_color()

    def has_declared(self):
        return self.color != None

    def anounce_main_color(self):
        self.announce({
            verb: COLOR,
            color: self.color
        })

    def add_bottom_to_dealer(self):
        self.cards[self.dealer].extend(self.deck.order[48:54])
        self.tell(self.dealer, {
            verb: BOTTOM,
            cards: self.deck.order[48:54]
        })

    def dealer_selected_bottom(self):
        return self.bottom != []
    
    def dealer_select_bottom(self, player, bottom):
        if player != self.dealer:
            self.tell(player, {verb: REJECT})
            return
        if len(bottom) != 6:
            self.tell(player, {verb: REJECT})
            return
        for i in bottom:
            if i not in self.cards[self.dealer]:
                self.tell(player, {verb: REJECT})
                return
        self.bottom = bottom
        for i in bottom:
            self.cards[self.dealer].remove(i)
        self.tell(player, {verb: ACK, bottom: self.bottom})

    def default_select_bottom(self):
        self.dealer_select_bottom(self.dealer, self.choose_least_cards(self.dealer, 6, None))

    def announce_player_play(self):
        self.announce({
            verb: PLAY,
            round_cards: self.round_cards,
            current_player: self.current_player
        })

    def player_play(self, player, cards):
        if player != self.current_player:
            self.tell(player, {verb: REJECT})
            return
        if any([card not in self.cards[player] for card in cards]):
            self.tell(player, {verb: REJECT})
            return
        if len(cards) == 0:
            self.tell(player, {verb: REJECT})
            return
        if player == self.round_winner:
            # first play in a round
            if len(cards) > 1:
                if any([self.is_main_card(card) for card in cards]):
                    self.tell(player, {verb: REJECT})
                    return
                colors = set([self.deck.color(card) for card in cards])
                if len(colors) != 1:
                    self.tell(player, {verb: REJECT})
                    return
        else:
            # follow
            required = len(self.round_cards[self.round_winner])
            mark = self.round_cards[self.round_winner][0]
            if len(cards) != required:
                self.tell(player, {verb: REJECT})
            played = self.cards_of_color(cards, mark)
            owned = self.cards_of_color(self.cards[player], mark)
            if played < required and played < owned:
                self.tell(player, {verb: REJECT})
                return
        self.round_cards[player] = cards

    def default_player_play(self):
        if self.current_player == self.round_winner:
            self.choose_least_cards(self.current_player, 1, None)
        else:
            self.choose_least_cards(self.current_player, len(self.round_cards[self.round_winner]), self.round_cards[self.round_winner][0])

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
        if !self.is_dealer_team(res):
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
            verb: SCORE,
            winner: self.round_winner,
            round_score: self.round_score,
            total_score: self.score
        })

    def bottom_scoring(self):
        score = 0
        if !self.is_dealer_team(self.round_winner):
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
            verb: SCORE,
            winner: self.round_winner,
            round_score: self.round_score,
            total_score: self.score
        })

    def announce(self, obj):
        print("Announce:", obj)

    def tell(self, player, obj):
        print("Tell player", player, ":", obj)

    def is_main_card(self, card_id):
        card = self.deck.card(card_id)
        if self.color == card[0]:
            return True
        if 'JOKER' == card[1] or '2' == card[1] or level == card[1]:
            return True
        return false
    
    def cards_of_color(self, cards, card_id):
        res = []
        if self.is_main_card(card_id):
            for i in cards:
                if self.is_main_card(i):
                    res.append(i)
        else:
            for i in cards:
                if self.deck.card(card_id)[0] == self.deck.card(i)[0]
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
        return max([value_of_card(card) for card in cards])

    def is_dealer_team(self, player):
        return (self.dealer + 0) % 4 or res == (self.dealer + 2) % 4

    def choose_least_cards(self, player, number, card_for_color):
        res = []
        if color != None:
            coc = self.cards_of_color(self.cards[player], card_for_color)
            coc.sort(reverse = True, key = self.value_of_card)
            num = min(len(coc), number)
            res.extend(coc[0:num])
            number -= num
        if number:
            cards = [i for i in self.cards[player] if  i not in res]
            cards.sort(reverse = True, key = self.value_of_card)
            res.extend(card[0, number])
        return res

class Match:
    pass
