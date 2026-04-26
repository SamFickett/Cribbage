"""
Samuel Fickett
April 26th, 2026

This script is an upgrade on Cribbage.py, which better
suits the web application. All globals are removed, as well as
print() and input().
"""

import numpy as np
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
            # wait for user_discard()
            pass
        elif self.state == GameState.CUT:
            self.cut()
            self.state = GameState.PEGGING

    def __init__(self):
        self.hand_cpu = []
        self.hand_user = []
        self.hand_crib = []

        self.user_pts = 0
        self.cpu_pts = 0
        self.user_crib = True
        
        self.state = GameState.START

        self.in_play = []
        self.count = 0

    # Game Flow
    def start_game(self):
        self.user_crib = random.choice([True, False])

        return 0
       
    def start_round(self):
        deck = self.create_deck()
        random.shuffle(deck)

        for _ in range(6):
            self.hand_cpu.append(deck.pop())
            self.hand_user.append(deck.pop())

        self.hand_cpu = []
        self.hand_user = []
        self.hand_crib = []
        self.in_play = []
        self.count = 0

        return 0

    # Crib
    def cpu_discard(self):
        return 0

    def user_discard(self, indices):
        return 0

    def cut(self):
        return 0

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