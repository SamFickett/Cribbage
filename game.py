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
from collections import Counter

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

        elif self.state == GameState.SCORING:
            result = self.score_round()
            self.reset_round()
            return result

        return {
            "state": self.state,
            "user_hand": self.hand_user,
            "cpu_hand": self.hand_cpu,
            "crib": self.hand_crib,
            "cut_card": getattr(self, "cut_card", None),
            "user_pts": self.user_pts,
            "cpu_pts": self.cpu_pts
        }

    def swap_crib(self):
        if self.dealer == "USER":
            self.dealer = "CPU"
        else:
            self.dealer = "USER"

        self.user_crib = (self.dealer == "USER")

    def reset_round(self):
        self.hand_cpu = []
        self.hand_user = []
        self.hand_crib = []
        self.in_play = []
        self.count = 0
        self.cut_card = None

        self.state = GameState.DEAL

    def __init__(self):
        self.hand_cpu = []
        self.hand_user = []
        self.hand_crib = []
        self.deck = []

        self.user_pts = 0
        self.cpu_pts = 0

        self.dealer = None
        self.user_crib = None

        self.current_turn = None
        self.last_player = None
        self.go_player = None
        
        self.state = GameState.START

        self.in_play = []
        self.count = 0

    # Game Flow
    def start_game(self):
        self.dealer = random.choice(["USER", "CPU"])
        self.user_crib = (self.dealer == "USER")
       
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

    # Cut
    def cut(self):
        self.cut_card = self.deck.pop()

        if self.cut_card[0] == "J":
            if self.user_crib:
                self.user_pts += 2
            else:
                self.cpu_pts += 2
        
        if self.user_crib:
            self.current_turn = "CPU"
        else:
            self.current_turn = "USER"

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
        if not self.can_play(self.hand_user):
            self.go_player = "USER"
            if self.can_play(self.hand_cpu):
                self.current_turn = "CPU"

                return {
                    "message": "User goes",
                    "count": self.count,
                }
            
            self.last_card_pts()
            self.reset_pegging()

        # REMOVE LATER
        playable = self.playable_cards(self.hand_user)
        card = playable.pop(0)
        # card = self.hand_user[index]

        if not self.is_valid_card(card):
            return {
                "error": "Card exceeds 31"
            }
        
        self.hand_user.remove(card)

        self.in_play.append(card)
        self.count += self.pcard_value(card)

        self.current_turn = "CPU"
        self.last_player = "USER"

        score = self.score_pegging()

        return {
            "played_card": card,
            "count": self.count,
            "in_play": self.in_play,
            "hand_user": self.hand_user,
            "score": score,
            "user_pts": self.user_pts
        }

    def play_cpu_card(self):
        if not self.can_play(self.hand_cpu):
            self.go_player = "CPU"
            if self.can_play(self.hand_user):
                self.current_turn = "USER"

                return {
                    "message": "CPU goes",
                    "count": self.count,
                }
            
            self.last_card_pts()
            self.reset_pegging()

        playable = self.playable_cards(self.hand_cpu)
        card = playable.pop(0)
        self.hand_cpu.remove(card)
        if not self.is_valid_card(card):
            return {
                "error": "Card exceeds 31"
            }

        self.in_play.append(card)
        self.count += self.pcard_value(card)

        self.current_turn = "USER"
        self.last_player = "CPU"

        score = self.score_pegging()

        return {
            "played_card": card,
            "count": self.count,
            "in_play": self.in_play,
            "hand_cpu": self.hand_cpu,
            "score": score,
            "cpu_pts": self.cpu_pts
        }

    def can_play(self, hand):
        for card in hand:
            value = self.pcard_value(card)
            if (value + self.count <= 31):
                return True
        
        return False
    
    def playable_cards(self, hand):
        return [card for card in hand if self.is_valid_card(card)]

    def is_valid_card(self, card):
        return self.pcard_value(card) + self.count <= 31

    def last_card_pts(self):
        pts = 2 if self.count == 31 else 1
        if self.last_player == "USER":
            self.user_pts += pts
        else:
            self.cpu_pts += pts        

    def score_pegging(self):
        pts = 0
        breakdown = []

        if self.check_15(self.in_play):
            pts += 2
            breakdown.append("15")

        pair_pts = self.check_pairs(self.in_play)
        if pair_pts:
            pts += pair_pts
            breakdown.append(f"pair:{pair_pts}")

        run_pts = self.check_runs(self.in_play)
        if run_pts:
            pts += run_pts
            breakdown.append(f"run:{run_pts}")

        if self.last_player == "USER":
            self.user_pts += pts
        else:
            self.cpu_pts += pts

        return {
            "points": pts,
            "breakdown": breakdown
        }

    def reset_pegging(self):
        self.in_play.clear()
        self.count = 0
        self.go_player = None
        self.current_turn = self.last_player

        if len(self.hand_user) == 0 and len(self.hand_cpu) == 0:
            self.state = GameState.SCORING

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
        if len(in_play) < 2:
            return 0
        
        last_rank = in_play[-1][0]
        matches = 1

        for card in reversed(in_play[:-1]):
            if card[0] == last_rank:
                matches += 1
            else:
                break

        if matches == 2:
            return 2
        elif matches == 3:
            return 6
        elif matches == 4:
            return 12
            
        return 0

    def is_run(self, cards):
        values = sorted(self.pcard_value(c) for c in cards)
        return all(values[i] + 1 == values[i + 1] for i in range(len(values) - 1))

    def check_runs(self, in_play):
        values = [self.scard_value(card) for card in in_play]

        for run_len in range(len(in_play), 2, -1):
            for combo in combinations(values, run_len):
                if self.is_run(combo):
                    return run_len
        
        return 0

    def pcard_value(self, card):
        # Peggin Card Values: A = 1, 2-10 as numbered, J/Q/K = 10
        if card.startswith("10"):
            return 10
        
        rank = card[0]

        if rank in self.LTR_CARDS:
            value = self.LTR_VALUES[rank]
            return min(value, 10)

        return int(rank)
    

    # Scoring
    def score_round(self):
        user_score = self.score_hand(self.hand_user, False)
        cpu_score = self.score_hand(self.hand_cpu, False)
        crib_score = self.score_hand(self.hand_crib, True)

        if self.user_crib:
            self.cpu_pts += cpu_score["total"]
            self.user_pts += user_score["total"] + crib_score["total"]
        else:
            self.user_pts += user_score["total"]
            self.cpu_pts += cpu_score["total"] + crib_score["total"]
        
        result = {
            "user_hand_score": user_score,
            "cpu_hand_score": cpu_score,
            "crib_score": crib_score,
            "user_total_pts": self.user_pts,
            "cpu_total_pts": self.cpu_pts
        }

        return result

    def score_hand(self, hand, is_user_crib):
        total = 0
        breakdown = {}
        full_hand = hand + [self.cut_card]

        pairs = self.score_pairs(full_hand)
        fifteens = self.score_fifteens(full_hand)
        runs = self.score_runs(full_hand)
        flush = self.score_flush(hand, self.cut_card, is_user_crib)
        nobs = self.score_nobs(hand, self.cut_card)

        breakdown["pairs"] = pairs
        breakdown["fifteens"] = fifteens
        breakdown["runs"] = runs
        breakdown["flush"] = flush
        breakdown["nobs"] = nobs

        total = sum(breakdown.values())

        return {
            "total": total,
            "breakdown": breakdown
        }
    
    def scard_value(self, card):
        # Scoring Card Values: A-K as 1-13, for runs

        if card.startswith("10"):
            return 10
        
        rank = card[0]

        if rank in self.LTR_CARDS:
            value = self.LTR_VALUES[rank]
            return value

        return int(rank)
    
    def score_pairs(self, hand):
        ranks = [self.scard_value(card) for card in hand]

        counts = Counter(ranks)

        pts = 0
        for count in counts.values():
            if count == 2:
                pts += 2
            elif count == 3:
                pts += 6
            elif count == 4:
                pts += 12
        
        return pts

    def score_fifteens(self, hand):
        # pcard_values -> J, Q, K count as 10 for 15s, but not for runs

        card_values = [self.pcard_value(card) for card in hand]

        pts = 0
        for r in range(2, len(hand) + 1):  # Check all combinations of 2 to 5 cards
            for combo in combinations(card_values, r):
                if sum(combo) == 15:
                    pts += 2

        return pts
    
    def is_run(self, values):
        values = sorted(int(v) for v in values)

        return all(values[i] + 1 == values[i + 1] for i in range(len(values) - 1))

    def score_runs(self, hand):
        values = [self.scard_value(card) for card in hand]

        for run_len in range(5, 2, -1):
            runs = []
            for combo in combinations(values, run_len):
                if self.is_run(combo):
                    runs.append(combo)
            if runs:
                return run_len * len(runs)  # Score is run length times number of runs
        
        return 0

    def score_flush(self, hand, cut, is_user_crib):
        suits = [card[-1] for card in hand]

        if len(set(suits)) != 1:
            return 0
        
        if is_user_crib:
            return 5 if cut[-1] == suits[0] else 0

        if cut[-1] == suits[0]:
            return 5
        return 4
    
    def score_nobs(self, hand, cut):
        cut_suit = cut[-1]

        for card in hand:
            if card[0] == "J" and card[-1] == cut_suit:
                return 1
            
        return 0