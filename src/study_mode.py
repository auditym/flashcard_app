import random
from card_manager import get_cards


class StudySession:
    def __init__(self, deck=None):
        # Load all cards or filter by deck
        all_cards = get_cards()
        if deck:
            self.cards = [c for c in all_cards if c["deck"] == deck]
        else:
            self.cards = all_cards

        self.index = 0
        self.showing_front = True

    def current_card(self):
        if not self.cards:
            return None
        return self.cards[self.index]

    def flip(self):
        self.showing_front = not self.showing_front

    def next_card(self):
        if self.cards:
            self.index = (self.index + 1) % len(self.cards)
            self.showing_front = True

    def prev_card(self):
        if self.cards:
            self.index = (self.index - 1) % len(self.cards)
            self.showing_front = True

    def shuffle(self):
        if self.cards:
            random.shuffle(self.cards)
            self.index = 0
            self.showing_front = True
