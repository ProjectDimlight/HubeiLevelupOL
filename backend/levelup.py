class Game:
    def __init__(dealer, dealer_level, deck):
        self.dealer = dealer
        self.level = banker_level
        self.deck = deck

        self.bottom = []
        self.cards = [[], [], [], []]
        self.round_winner = dealer

    def wait(seconds, cond, default_op):
        pass

    def game_play():
        deal_cards()
        wait(5, self.has_declared, self.default_declare)
        self.anounce_main_color()

        self.add_bottom_to_dealer()
        wait(30, self.dealer_selected_bottom, self.ai_select_bottom)

        while len(self.cards[self.round_winner]):
            self.ask_player_play()
            wait(20, player_played)
            

    def deal_cards():
        t = dealer
        for i in range(48):
            self.deal_card_to_player(t, self.deck.order[i])
            t = (t + 1) % 4

    def deal_card_to_player(player, card_id):
        pass

    def declare(player, card_id):
        card = self.deck.card(card_id)
        if self.level == card[1]:
            self.color = card[0]

    def default_declare():
        card = self.deck.card(50)
        self.color = card[0]

    def has_declared():
        return self.color != None

    def anounce_main_color():
        pass

    def 

class Match:
    pass
