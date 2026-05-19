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

            return self.build_state(last_action = {
                "type": "start_game",
                "dealer": self.dealer
            })

        elif self.state == GameState.DEAL:
            self.start_round()
            self.state = GameState.DISCARD

            return self.build_state(last_action = {
                "type": "deal",
                "dealer": self.dealer,
                "user_crib": self.user_crib
            })

        elif self.state == GameState.DISCARD:
            if len(self.hand_crib) == 4:
                self.state = GameState.CUT

                return self.build_state(last_action = {
                    "type": "discard_complete",
                    "crib": self.hand_crib
                })

        elif self.state == GameState.CUT:
            return self.build_state(last_action = {
                "type": "awaiting_cut"
            })

        elif self.state == GameState.PEGGING:
            return self.build_state(last_action = {
                "type": "awaiting_pegging",
                "current_turn": self.current_turn
            })

        elif self.state == GameState.SCORING:
            result = self.score_round()
            self.end_round()

            return self.build_state(last_action = {
                "type": "round_score",
                "result": result
            })

        return self.build_state()

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

        self.round_state = {
            "user_hand": self.hand_user.copy(),
            "cpu_hand": self.hand_cpu.copy(),
            "crib": self.hand_crib.copy(),
            "cut_card": None
        }

        return {
            "hand_user": self.hand_user,
            "hand_cpu": self.hand_cpu,
            "state": self.state
        }

    def end_round(self):
        self.swap_crib()
        self.reset_round()
        self.round_state = None

    # Crib
    def cpu_discard(self):
        if not self.hand_cpu:
            raise Exception("CPU hand is empty")
        
        possible_hands = combinations(self.hand_cpu, 4)

        best_score = -1
        best_hand = None
        
        # Evaluate for best possible hand
        for hand in possible_hands:
            score = self.eval_hand(list(hand))

            if score > best_score:
                best_score = score
                best_hand = list(hand)

        # Discard
        remaining = best_hand.copy()
        discard = []

        for card in self.hand_cpu:
            if card in remaining:
                remaining.remove(card)
            else:
                discard.append(card)

        self.hand_cpu = best_hand
        self.hand_crib.extend(discard)

        self.round_state["cpu_hand"] = self.hand_cpu.copy()

        return self.build_state(last_action = {
            "type": "discard",
            "player": "CPU",
            "cards": discard
        })

    # CPU Discard logic
    def eval_hand(self, cards):
        score = 0
        values = [self.scard_value(card) for card in cards]

        # Value 15's the highest
        for value in values:
            if value == 5:
                score += 5
            elif value >= 10:
                score += 2

        # Pairs next
        counts = Counter(values)
        for count in counts.values():
            if count == 2:
                score += 3

        # Potential Runs last
        sorted_vals = sorted(values)
        for i in range(len(sorted_vals) - 1):
            if sorted_vals[i + 1] - sorted_vals[i] == 1:
                score += 2
        
        return score

    def user_discard(self, indices):
        if not self.hand_user:
            raise Exception("User hand is empty")

        removed = []

        for i in sorted(indices, reverse = True):
            removed.append(self.hand_user.pop(i))

        self.hand_crib.extend(removed)

        self.round_state["user_hand"] = self.hand_user.copy()
        self.round_state["crib"] = self.hand_crib.copy()

        self.state = GameState.CUT

        return self.build_state(last_action = {
            "type": "discard",
            "player": "USER",
            "cards": removed
        })

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

        self.round_state["cut_card"] = self.cut_card

        # return self.cut_card
        return self.build_state(last_action = {
            "type": "cut",
            "card": self.cut_card,
            "points_scored": 2 if self.cut_card[0] == "J" else 0
        })

    # Pegging
    def play_user_card(self, index):
        if not self.can_play(self.hand_user):
            self.go_player = "USER"
            if self.can_play(self.hand_cpu):
                self.current_turn = "CPU"

                return self.build_state(last_action = {
                "type": "go",
                "player": "USER",
                "reason": "no playable cards"
                })
            
            self.last_card_pts()
            self.reset_pegging()

            return self.build_state(last_action = {
                "type": "go_reset",
                "player": "USER",
                "reason": "no playable cards"
            })

        card = self.hand_user[index]
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

        return self.build_state(last_action = {
            "type": "play_card",
            "player": self.last_player,
            "card": card,
            "count_after": self.count,
            "points_scored": score["points_scored"]
        })
    
    # User helper function (UI Helper)
    def get_playable_indices(self, hand):
            return [i for i, card in enumerate(hand) if self.is_valid_card(card)] 

    def play_cpu_card(self):
        if not self.can_play(self.hand_cpu):
            self.go_player = "CPU"
            if self.can_play(self.hand_user):
                self.current_turn = "USER"

                return self.build_state(last_action = {
                "type": "go",
                "player": "CPU",
                "reason": "no playable cards"
                })
            
            self.last_card_pts()
            self.reset_pegging()

            return self.build_state(last_action = {
                "type": "go_reset",
                "player": "CPU",
                "reason": "no playable cards"
            })

        playable = self.playable_cards(self.hand_cpu)
        card = max(playable, key = self.eval_pegging_card)

        self.hand_cpu.remove(card)
        self.in_play.append(card)
        self.count += self.pcard_value(card)

        self.current_turn = "USER"
        self.last_player = "CPU"

        score = self.score_pegging()

        return self.build_state(last_action = {
            "type": "play_card",
            "player": self.last_player,
            "card": card,
            "count_after": self.count,
            "points_scored": score["points_scored"]
        })
    
    def eval_pegging_card(self, card):
        temp_in_play = self.in_play + [card]
        score = 0

        if self.check_15(temp_in_play):
            score += 2
        
        score += self.check_pairs(temp_in_play)
        score += self.check_runs(temp_in_play)

        if self.count + self.pcard_value(card) == 31:
            score += 2

        return score

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

        scorer = self.last_player
        return {
            "points_scored": pts,
            "scorer": scorer
        }

    def reset_pegging(self):
        self.in_play.clear()
        self.count = 0
        self.go_player = None
        # self.current_turn = self.last_player

        if self.pegging_over():
            self.state = GameState.SCORING

    def pegging_over(self):
        return len(self.hand_user) == 0 and len(self.hand_cpu) == 0

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
        user_score = self.score_hand(self.round_state["user_hand"], False)
        cpu_score = self.score_hand(self.round_state["cpu_hand"], False)
        crib_score = self.score_hand(self.round_state["crib"], True)

        if self.user_crib:
            self.cpu_pts += cpu_score["total"]
            self.user_pts += user_score["total"] + crib_score["total"]
        else:
            self.user_pts += user_score["total"]
            self.cpu_pts += cpu_score["total"] + crib_score["total"]

        return self.build_state(last_action = {
            "type": "round_score",
            "user_scored": user_score,
            "cpu_scored": cpu_score,
            "crib_scored": crib_score
        })

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
    
    # UI Helpers
    def build_state(self, last_action = None):
        return {
            "state": self.state,
            "turn": self.current_turn,

            "user_hand": self.hand_user,
            "cpu_hand": self.hand_cpu,
            "crib": self.hand_crib,

            "count": self.count,
            "in_play": self.in_play,

            "cut_card": getattr(self, "cut_card", None),

            "user_pts": self.user_pts,
            "cpu_pts": self.cpu_pts,

            "legal_moves": {
                "user": self.get_playable_indices(self.hand_user),
                "cpu": self.get_playable_indices(self.hand_cpu)
            },

            "last_action": last_action
        }