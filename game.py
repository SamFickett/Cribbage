"""
Samuel Fickett
April 26th, 2026

This script is an upgrade on Cribbage.py, which better
suits the web application. All globals are removed, as well as
print() and input().
"""

# import numpy as np
import random
from itertools import combinations

# Initializes game states
class GameState:
    START = "START"
    DEAL = "DEAL"
    DISCARD = "DISCARD"
    CUT = "CUT"
    PEGGING = "PEGGING"
    SCORING = "SCORING"

class CribbageGame:
    LTR_CARDS = {"A", "J", "Q", "K"}
    LTR_VALUES = {
        "A": 1,
        "J": 11,
        "Q": 12,
        "K": 13
    }

    RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    SUITS = ["H", "D", "C", "S"]

    def create_deck(self):
        return [rank + suit for suit in self.SUITS for rank in self.RANKS]

    def step(self):
        if self.state == GameState.START:
            self.start_game()
            self.state = GameState.DEAL

        elif self.state == GameState.DEAL:
            self.start_round()
            self.state = GameState.DISCARD

        elif self.state == GameState.DISCARD:
            if len(self.hand_crib) == 4:
                self.state = GameState.CUT

        elif self.state == GameState.CUT:
            pass

        elif self.state == GameState.PEGGING:
            pass


        return {
            "state": self.state,
            "user_hand": self.hand_user,
            "cpu_hand": self.hand_cpu,
            "crib": self.hand_crib,
            "cut_card": getattr(self, "cut_card", None),
            "user_pts": self.user_pts,
            "cpu_pts": self.cpu_pts
        }

    def reset_round(self):
        self.hand_cpu = []
        self.hand_user = []
        self.hand_crib = []
        self.in_play = []
        self.count = 0
        self.cut_card = None

        self.state = GameState.START

    def __init__(self):
        self.hand_cpu = []
        self.hand_user = []
        self.hand_crib = []
        self.deck = []

        self.user_pts = 0
        self.cpu_pts = 0
        self.user_crib = True
        
        self.state = GameState.START

        self.in_play = []
        self.count = 0

    # Game Flow
    def start_game(self):
        self.user_crib = random.choice([True, False])
       
    def start_round(self):
        if self.state != GameState.DEAL:
            raise Exception("Invalid state for dealing")

        self.deck = self.create_deck()
        random.shuffle(self.deck)

        self.hand_cpu = []
        self.hand_user = []
        self.hand_crib = []
        self.in_play = []
        self.count = 0

        for _ in range(6):
            self.hand_cpu.append(self.deck.pop())
            self.hand_user.append(self.deck.pop())

        return {
            "hand_user": self.hand_user,
            "hand_cpu": self.hand_cpu,
            "state": self.state
        }

    # Crib
    def cpu_discard(self):
        if not self.hand_cpu:
            raise Exception("CPU hand is empty")

        random.shuffle(self.hand_cpu)
        discarded = self.hand_cpu[:2]
        self.hand_cpu = self.hand_cpu[2:]
        self.hand_crib.extend(discarded)

        return {
            "hand_cpu": self.hand_cpu,
            "hand_crib": self.hand_crib,
            "state": self.state
        }

    def user_discard(self, indices):
        if not self.hand_user:
            raise Exception("User hand is empty")

        removed = []

        for i in sorted(indices, reverse = True):
            removed.append(self.hand_user.pop(i))

        self.hand_crib.extend(removed)
        self.state = GameState.CUT

        return {
            "hand_user": self.hand_user,
            "hand_cpu": self.hand_cpu,
            "hand_crib": self.hand_crib,
            "state": self.state
        }

    def cut(self):
        self.cut_card = self.deck.pop()

        if self.cut_card[0] == "J":
            if self.user_crib:
                self.user_pts += 2
            else:
                self.cpu_pts += 2
        
        self.state = GameState.PEGGING

        # return self.cut_card
        return {
            "cut_card": self.cut_card,
            "user_pts": self.user_pts,
            "cpu_pts": self.cpu_pts,
            "state": self.state
        }

    # Pegging
    def play_user_card(self, index):
        return 0

    def play_cpu_card(self):
        return 0

    def can_play(self, hand):
        return 0

    # Scoring
    def scoring(self, hand, player):
        return 0

    # Helpers
    def check_15(self, in_play):
        total = 0

        for card in in_play:
            number = card[0]

            if len(card) == 3:
                total += 10
            elif number in self.LTR_CARDS:
                value = self.LTR_VALUES[number]
                if value > 10:
                    value = 10
                total += value
            else:
                total += int(number)

        return total == 15

    def check_pairs(self, in_play):
        def pair(in_play):
            c1 = in_play[-1]
            c2 = in_play[-2]

            return c1[0] == c2[0]
        
        def three_kind(in_play):
            c1 = in_play[-1]
            c2 = in_play[-2]
            c3 = in_play[-3]

            return c1[0] == c2[0] == c3[0]

        def four_kind(in_play):
            c1 = in_play[-1]
            c2 = in_play[-2]
            c3 = in_play[-3]
            c4 = in_play[-4]

            return c1[0] == c2[0] == c3[0] == c4[0]

        if len(in_play) >= 4:
            if four_kind(in_play):
                return 12
            if three_kind(in_play):
                return 6
            if pair(in_play):
                return 2
        elif len(in_play) == 3:
            if three_kind(in_play):
                return 6
            if pair(in_play):
                return 2
        elif len(in_play) == 2:
            if pair(in_play):
                return 2
            
        return 0

    def is_run(self, cards):
        values = sorted(self.card_value(c) for c in cards)
        return all(values[i] + 1 == values[i + 1] for i in range(len(values) - 1))

    def check_runs(self, in_play):
        for run_len in range(len(in_play), 2, -1):
            for combo in combinations(in_play, run_len):
                if self.is_run(combo):
                    return run_len
        
        return 0

    def card_value(self, card):
        if card.startswith("10"):
            return 10
        
        rank = card[0]

        if rank in self.LTR_CARDS:
            value = self.LTR_VALUES[rank]
            return min(value, 10)

        return int(rank)