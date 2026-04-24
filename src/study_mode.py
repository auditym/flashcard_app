import random
from src.card_manager import get_cards

class StudySession:
    def __init__(self, deck=None):
        self.cards = get_cards(deck)
        self.index = 0
        self.showing_front = True

    def current_card(self):
        if not self.cards:
            return None
        return self.cards[self.index]

    def flip(self):
        self.showing_front = not self.showing_front

    def next_card(self):
        if not self.cards:
            return None
        self.index = (self.index + 1) % len(self.cards)
        self.showing_front = True

    def prev_card(self):
        if not self.cards:
            return None
        self.index = (self.index - 1) % len(self.cards)
        self.showing_front = True

    def shuffle(self):
        random.shuffle(self.cards)
        self.index = 0
        self.showing_front = True
