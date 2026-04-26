import numpy as np
import random
from collections import Counter
from itertools import combinations

# Each hand
hand_CPU = []
hand_USER = []
hand_crib = []

# Point totals and crib boolean
USER_points = 0
CPU_points = 0
USER_crib = True

# The suits
hearts = ["AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH"]
diamonds = ["AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD"]
spades = ["AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS"]
clubs = ["AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC"]

# Library for letter cards
ltr_cards = "AJQK"
ltr_cards_dict = {
    "A": 1,
    "J": 11,
    "Q": 12,
    "K": 13
}

# Creating the deck
cards = []
for i in hearts:
    cards.append(i)
for i in diamonds:
    cards.append(i)
for i in spades:
    cards.append(i)
for i in clubs:
    cards.append(i)

# Cuts the cards, lower card earns crib first
def start_game(cards):
    # USER and CPU draw a card each
    cards_copy = cards.copy()
    draw_USER = random.choice(cards_copy)
    cards_copy.remove(draw_USER)
    draw_CPU = random.choice(cards_copy)

    user_val = 0
    cpu_val = 0

    # Is card a letter card
    if (len(draw_USER) == 3):
        user_val = 10
    elif draw_USER[0] in ltr_cards:
        user_val = ltr_cards_dict[draw_USER[0]]
    else:
        user_val = int(draw_USER[0])

    if (len(draw_CPU) == 3):
        cpu_val = 10
    elif draw_CPU[0] in ltr_cards:
        cpu_val = ltr_cards_dict[draw_CPU[0]]
    else:
        cpu_val = int(draw_CPU[0])

    # Who gets the crib
    if user_val < cpu_val:
        return True
    elif user_val > cpu_val:
        return False
    else:
        # Run again if both cards have the same value
        return start_game(cards)

# Dealing the cards, whoever has the crib deals.
# Dealer gets dealt after their opponent
def start_round(cards):
    cards_copy = cards.copy()
    if not USER_crib:
        for i in range(6):
            draw = random.choice(cards_copy)
            hand_USER.append(draw)
            cards_copy.remove(draw)

            draw = random.choice(cards_copy)
            hand_CPU.append(draw)
            cards_copy.remove(draw)
    else:
        for i in range(6):
            draw = random.choice(cards_copy)
            hand_CPU.append(draw)
            cards_copy.remove(draw)

            draw = random.choice(cards_copy)
            hand_USER.append(draw)
            cards_copy.remove(draw)

# Creating the crib, each player discards two cards.
# This crib will be counted for points after pegging
def build_crib():
    # Here is the logic for the CPU discard
    # It values 5's, 10's, and face cards, as those are easy two points
    t = 0
    x = random.choice(hand_CPU)
    x_val = 0
    if x[0] in ltr_cards:
        x_val = ltr_cards_dict[x[0]]
    else:
        x_val = int(x[0])

    # This decides which card to get rid of. If 5 or 10+, they try again, up to a total of 12 times
    while (x_val == 5 or x_val == 1 or t > 12):
        x = random.choice(hand_CPU)
        if x[0] in ltr_cards:
            x_val = ltr_cards_dict[x[0]]
        else:
            x_val = int(x[0])
        t += 1
    hand_CPU.remove(x)
    hand_crib.append(x)

    # Rince and repeat for the second card
    t = 0
    y = random.choice(hand_CPU)
    y_val = 0
    if y[0] in ltr_cards:
        y_val = ltr_cards_dict[y[0]]
    else:
        y_val = int(y[0])
    while (y_val == 5 or y_val == 1 or t > 12):
        y = random.choice(hand_CPU)
        if y[0] in ltr_cards:
            y_val = ltr_cards_dict[y[0]]
        else:
            y_val = int(y[0])
        t += 1
    hand_CPU.remove(y)
    hand_crib.append(y)

    # This runs the script that prompts the user to discard two cards
    def USERS_hand():
        str = "\"[card1, card2]\""
        crib = ""
        if not USER_crib:
           crib = "It's the CPU's crib"
        else:
           crib = "It's your crib"

        print("Here is your dealt hand.", end=" ")
        print(crib)
        print(hand_USER)
        print("Please select two cards to discard, choose numbers 1-6. (ex: 2, 5)")
        discard_list = input()
        a = 1
        c1 = int(discard_list[0])
        c2 = int(discard_list[-1])
        
        condition2 = c1 > 6 or c1 < 1
        condition3 = c2 > 6 or c2 < 1
    
        if condition2:
            c1 = 1 
        if condition3:
            c2 = 2 
        
        condition1 = c1 == c2
        if not (condition1) and not (condition2 or condition3):
            c1 = int(discard_list[0])
            c2 = int(discard_list[-1])
        if condition1:
            c1 = 1
            c2 = 2
        


        print("\nAre you sure you want to discard these cards? (y/n)")
        print(hand_USER[c1 - 1], end=" and ")
        print(hand_USER[c2 - 1])
        confirm_discard = input()
    
        if confirm_discard == "n" or  not confirm_discard:
            USERS_hand()
        else:
            card1 = hand_USER[int(discard_list[0]) - 1]
            card2 = hand_USER[int(discard_list[-1]) - 1]
            hand_crib.append(card1)
            hand_crib.append(card2)
            hand_USER.remove(card1)
            hand_USER.remove(card2)
    
    USERS_hand()

# Sets the deck
def set_deck(bool=False, cut=""):
    cards_copy = cards.copy()
    for card in hand_USER:
        cards_copy.remove(card)
    for card in hand_CPU:
        cards_copy.remove(card)
    for card in hand_crib:
        cards_copy.remove(card)
    if bool:
        cards_copy.remove(cut)
    return cards_copy

# Cuts the deck
# Returns the cut card
def cut():
    global USER_points
    global CPU_points

    cards_copy = set_deck()
    cut_card = random.choice(cards_copy)
    print(f"\nThe cut card is {cut_card}")


    if cut_card[0] == "J":
        if USER_crib:
            print(f"You cut the Jack. +2")
            USER_points += 2
        else:
            print(f"The CPU cut the Jack. +2")
            CPU_points += 2

    # Win conditions
    if USER_points >= 121:
        print(f"You have won! The score was {USER_points}-{CPU_points}")
    if CPU_points >= 121:
        print(f"You have lost. The score was {USER_points}-{CPU_points}")

    return cut_card
    
# Scoring, pegging pile
def check_15(in_play):
    a = 0
    for card in in_play:
        number = card[0]
        if len(card) == 3:
            a += 10
        elif number in ltr_cards:
            number = ltr_cards_dict[number]
            if number > 10:
                number = 10
            a += number
        else:
            a += int(number)

    if a == 15:
        return True
    else: 
        return False

def check_pairs(in_play):
    def pair(in_play):
        c1 = in_play[-1]
        c2 = in_play[-2]

        if c1[0] == c2[0]:
            return True
        else:
            return False
        
    def three_kind(in_play):
        c1 = in_play[-1]
        c2 = in_play[-2]
        c3 = in_play[-3]

        if c1[0] == c2[0] == c3[0]:
            return True
        else:
            return False

    def four_kind(in_play):
        c1 = in_play[-1]
        c2 = in_play[-2]
        c3 = in_play[-3]
        c4 = in_play[-4]

        if c1[0] == c2[0] == c3[0] == c4[0]:
            return True
        else:
            return False

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

def check_runs(in_play):
    sequence = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    # This is used to determine if the list of values is inside the sequence list
    def is_sublist(main_list, sublist):
        if not sublist:  # An empty list is always a sublist
            return True

        sublist_len = len(sublist)
        for i in range(len(main_list) - sublist_len + 1):
            if main_list[i:i + sublist_len] == sublist:
                return True
        return False
    
    # Checks for a continuous 7 card run
    def check_run7(in_play):
        cards = []
        if len(in_play) < 7:
            return False
        else:
            # Grabs just the value of each card
            for count, card in enumerate(in_play):
                if not count > 6:
                    cards.append(card[0])

            if is_sublist(sequence, cards):
                return True
            
            # Reverses the sequence
            sequence.reverse()
            if is_sublist(sequence, cards):
                return True
            
        # If reached, there was no run    
        return False
    # Checks for a continuous 6 card run
    def check_run6(in_play):
        cards = []
        if len(in_play) < 6:
            return False
        else: 
            # Grabs just the value of each card
            for count, card in enumerate(in_play):
                if not count > 5:
                    cards.append(card[0])

            if is_sublist(sequence, cards):
                return True
            
            # Reverses the sequence
            sequence.reverse()
            if is_sublist(sequence, cards):
                return True
            
        # If reached, there was no run
        return False
    # Checks for a continuous 5 card run
    def check_run5(in_play):
        cards = []
        if len(in_play) < 5:
            return False
        else: 
            # Grabs just the value of each card
            for count, card in enumerate(in_play):
                if not count > 4:
                    cards.append(card[0])

            if is_sublist(sequence, cards):
                return True
            
            # Reverses the sequence
            sequence.reverse()
            if is_sublist(sequence, cards):
                return True
            
        # If reached, there was no run
        return False
    # Checks for a continuous 4 card run
    def check_run4(in_play):
        cards = []
        if len(in_play) < 4:
            return False
        else: 
            # Grabs just the value of each card
            for count, card in enumerate(in_play):
                if not count > 3:
                    cards.append(card[0])

            if is_sublist(sequence, cards):
                return True
            
            # Reverses the sequence
            sequence.reverse()
            if is_sublist(sequence, cards):
                return True
            
        # If reached, there was no run
        return False
    # Checks for a 3 card run
    def check_run3(in_play):
        if len(in_play) < 3:
            return False
        else:
            c1 = in_play[-1]
            c2 = in_play[-2]
            c3 = in_play[-3]
            list = []

            if len(c1) == 3:
                list.append(10)
            elif c1[0] in ltr_cards:
                n = ltr_cards_dict[c1[0]]
                list.append(n)
            else: 
                list.append(int(c1[0]))

            if len(c2) == 3:
                list.append(10)
            elif c2[0] in ltr_cards:
                n = ltr_cards_dict[c2[0]]
                list.append(n)
            else: 
                list.append(int(c2[0]))
    
            if len(c3) == 3:
                list.append(10)
            elif c3[0] in ltr_cards:
                n = ltr_cards_dict[c3[0]]
                list.append(n)
            else: 
                list.append(int(c3[0]))

            list.sort()
            # Checks for three card run
            for count, number in enumerate(list):
                if count == 2:
                    continue
                if count + 1 > len(list):
                    continue
                else:
                    a = list[count+1] - number
                    if a == 1:
                        continue
                    else: 
                        return False
        
            # If this is reached, then the last three cards of the pegging pile were a three card run
            return True
    
    # How many, if any, points were gained
    if check_run7(in_play):
        return 7
    elif check_run6(in_play):
        return 6
    elif check_run5(in_play):
        return 5
    elif check_run4(in_play):
        return 4
    elif check_run3(in_play):
        return 3
    else:
        return 0

# Pegging stage of the game
def pegging(cut_card):
    global CPU_points
    global USER_points
    deck = set_deck(True, cut_card)
    count = 0
    in_play = []

    hand_CPU_copy = hand_CPU.copy()
    hand_USER_copy = hand_USER.copy()

    # Returns True if the hand is "unplayable"
    def can_play(hand):
        go_list = []
        for card in hand:
            if len(card) == 3:
                go_list.append("10")
            else:
                go_list.append(card[0])

        go_count = 0
        for number in go_list:
            if number in ltr_cards:
                number = ltr_cards_dict[number]
                if number > 10:
                    number = 10
            if int(number) > (31 - count):
                go_count += 1

        if go_count == len(go_list):
            return True
        else:
            return False

    def play_CPU(count):
        global CPU_points
        global USER_points
        card = random.choice(hand_CPU_copy)
        card_valid = False

        # Forces the valid card if can play and has ineligible card(s)
        while not card_valid:
            value = 0
            if len(card) == 3:
                value = 10
            elif card[0] in ltr_cards:
                n = ltr_cards_dict[card[0]]
                if n > 10:
                    n = 10
                value = n
            else:
                value = int(card[0])
                
            if count + value > 31:
                card = random.choice(hand_CPU_copy)
            else:
                card_valid = True

        in_play.append(card)
        hand_CPU_copy.remove(card)

        # Update count

        if card[0] in ltr_cards:
            n = ltr_cards_dict[card[0]]
            if n > 10:
                n = 10
            count += n
        else:
            if len(card) == 3:
                count += 10
            else:
                count += int(card[0])

        # Check Points
        # 15s
        if check_15(in_play):
            CPU_points += 2
            print(f"The CPU gained 2 points. They now have {CPU_points} points")
        if CPU_points > 121:
            print(f"CPU has won. Score: \n CPU: {CPU_points} \n You: {USER_points}")
            exit()

        # Pairs
        a = check_pairs(in_play)
        CPU_points += a
        if a != 0:
            print(f"The CPU gained {a} points. They now have {CPU_points} points")
        if CPU_points > 121:
            print(f"CPU has won. Score: \n CPU: {CPU_points} \n You: {USER_points}")
            exit()

        # Runs
        a = check_runs(in_play)
        CPU_points += a
        if a != 0:
            print(f"The CPU gained {a} points. They now have {CPU_points} points")
        if CPU_points > 121:
            print(f"CPU has won. Score: \n CPU: {CPU_points} \n You: {USER_points}")
            exit()

        print("The CPU has played a card")
        return count

    def play_USER(count):
        global CPU_points
        global USER_points
        print(f"Lay down one of your cards. ex. (1-{len(hand_USER_copy)})")
        print(hand_USER_copy)
        a = int(input())

        # Number not valid, computer choses first card in hand
        if a > len(hand_USER_copy):
            print("You made an invalid choice, the computer will chose for you")
            a = 1
            
        card = hand_USER_copy[a-1]

        condition = True
        c_value = 0
        # If chosen card is too large, pick again
        while condition:
            if len(card) == 3:
                c_value = 10
            elif card[0] in ltr_cards:
                n = ltr_cards_dict[card[0]]
                if n > 10:
                    n = 10
                c_value += n
            else:
                c_value += int(card[0])
            
            if c_value + count > 31:
                print(f"You made an invalid choice, your card was too large. the computer will chose for you")
                c = 0
                c_value = 0
                while True:
                    card = hand_USER_copy[c]
                    if len(card) == 3:
                        c_value = 10
                    elif card[0] in ltr_cards:
                        n = ltr_cards_dict[card[0]]
                        if n > 10:
                            n = 10
                        c_value += n
                    else:
                        c_value += int(card[0])
                    
                    if c_value + count > 31:
                        c += 1
                        c_value = 0
                    else:
                        condition = False
            else:
                condition = False
            
                

        in_play.append(card)
        hand_USER_copy.remove(card)

        # Update count

        if card[0] in ltr_cards:
            n = ltr_cards_dict[card[0]]
            if n > 10:                    
                n = 10
            count += n
        else:
            if len(card) == 3:
                count += 10
            else:
                count += int(card[0])

        # Check Points
        # 15s
        if check_15(in_play):
            USER_points += 2
            print(f"You gained 2 points. You now have {USER_points} points")
        if USER_points > 121:
            print(f"You win. Score: \n You: {USER_points} \n CPU: {CPU_points}")
            exit()

        # Pairs
        a = check_pairs(in_play)
        USER_points += a
        if a != 0:
            print(f"You gained {a} points. You now have {USER_points} points")
        if USER_points > 121:
            print(f"You win. Score: \n You: {USER_points} \n CPU: {CPU_points}")
            exit()

        # Runs
        a = check_runs(in_play)
        USER_points += a
        if a != 0:
            print(f"You gained {a} points. You now have {USER_points} points")
        if USER_points > 121:
            print(f"You win. Score: \n You: {USER_points} \n CPU: {CPU_points}")
            exit()
            
        return count

    print("The pegging pile is empty, the game has begun")

    # Runs through pegging until all cards have been played
    if USER_crib:
        while (len(hand_CPU_copy) != 0) or (len(hand_USER_copy) != 0):
            # Can CPU play a card
            if not can_play(hand_CPU_copy):
                count = play_CPU(count)
            else:
                # Can User play card, if so, let them
                # If not enter if statement
                if can_play(hand_USER_copy):
                    if count == 31:
                        USER_points += 2
                        print(f"You gained 2 points, you made the count 31. You now have {USER_points} points")
                        if USER_points > 121:
                            print(f"You win. Score: \n You: {USER_points} \n CPU: {CPU_points}")
                            exit()
                    else:
                        USER_points += 1
                        print(f"You gained 1 point, the CPU couldn't play another card. You now have {USER_points} points")
                        if USER_points > 121:
                            print(f"You win. Score: \n You: {USER_points} \n CPU: {CPU_points}")
                            exit()
                    in_play.clear()
                    count = 0
                    count = play_CPU(count)

            print(f"Here is the current pegging pile \n {in_play}")
            print(f"The count is {count}", end="\n\n")
             # Last card, gains one point if you play it
            if (len(hand_CPU_copy) == 0) and (len(hand_USER_copy) == 0):
                if count == 31:
                    CPU_points += 2
                    print(f"The CPU played last and made the count 31, they gained 2 points. They now have {CPU_points} points")
                    if CPU_points > 121:
                        print(f"CPU has won. Score: \n CPU: {CPU_points} \n You: {USER_points}")
                        exit()
                else:
                    CPU_points += 1
                    print(f"The CPU played last, they gained 1 point. They now have {CPU_points} points")
                    if CPU_points > 121:
                        print(f"CPU has won. Score: \n CPU: {CPU_points} \n You: {USER_points}")
                        exit()

                continue

            # Can you play a card
            if not can_play(hand_USER_copy):
                count = play_USER(count)
            else:
                # Can CPU play a card, if so, let them
                # If not enter if statement
                if can_play(hand_CPU_copy):
                    if count == 31:
                        CPU_points += 2
                        print(f"The CPU gained 2 points, they made the count 31. They now have {CPU_points} points.")
                        if CPU_points > 121:
                            print(f"CPU has won. Score: \n CPU: {CPU_points} \n You: {USER_points}")
                            exit()
                    else:
                        CPU_points += 1
                        print(f"The CPU gained 1 point, you couldn't play another card. They now have {CPU_points} points")
                        if CPU_points > 121:
                            print(f"CPU has won. Score: \n CPU: {CPU_points} \n You: {USER_points}")
                            exit()
                    in_play.clear()
                    count = 0
                    count = play_USER(count)
                    
            print(f"Here is the current pegging pile \n {in_play}")
            print(f"The count is {count}", end="\n\n")
            # Last card, gains one point if you play it
            if (len(hand_CPU_copy) == 0) and (len(hand_USER_copy) == 0):
                if count == 31:
                    USER_points += 2
                    print(f"You played last and made the count 31, you gained 2 points. You now have {USER_points} points")
                    if USER_points > 121:
                        print(f"You win. Score: \n You: {USER_points} \n CPU: {CPU_points}")
                        exit()
                else:
                    USER_points += 1
                    print(f"You played last, you gained 1 point. You now have {USER_points} points")
                    if USER_points > 121:
                        print(f"You win. Score: \n You: {USER_points} \n CPU: {CPU_points}")
                        exit()
                
                continue
    else:
        while (len(hand_CPU_copy) != 0) or (len(hand_USER_copy) != 0):
            # Can you play a card
            if not can_play(hand_USER_copy):
                count = play_USER(count)
            else:
                # Can CPU play a card, if so, let them
                # If not enter if statement
                if can_play(hand_CPU_copy):
                    if count == 31:
                        CPU_points += 2
                        print("The CPU gained 2 points, they made the count 31.")
                        if CPU_points > 121:
                            print(f"CPU has won. Score: \n CPU: {CPU_points} \n You: {USER_points}")
                            exit()
                    else:
                        CPU_points += 1
                        print("The CPU gained 1 point, you couldn't play another card")
                        if CPU_points > 121:
                            print(f"CPU has won. Score: \n CPU: {CPU_points} \n You: {USER_points}")
                            exit()
                    in_play.clear()
                    count = 0
                    count = play_USER(count)

            print(f"Here is the current pegging pile \n {in_play}")
            print(f"The count is {count}", end="\n\n")
            # Last card, gains one point if you play it
            if (len(hand_CPU_copy) == 0) and (len(hand_USER_copy) == 0):
                if count == 31:
                    USER_points += 2
                    print("You played last and made the count 31, you gained 2 points")
                    if USER_points > 121:
                        print(f"You win. Score: \n You: {USER_points} \n CPU: {CPU_points}")
                        exit()
                else:
                    USER_points += 1
                    print("You played last, you gained 1 point")
                    if USER_points > 121:
                        print(f"You win. Score: \n You: {USER_points} \n CPU: {CPU_points}")
                        exit()
                
                continue

            # Can CPU play a card
            if not can_play(hand_CPU_copy):
                count = play_CPU(count)
            else:
                # Can User play card, if so, let them
                # If not, enter if statement
                if can_play(hand_USER_copy):
                    if count == 31:
                        USER_points += 2
                        print("You gained 2 points, you made the count 31.")
                        if USER_points > 121:
                            print(f"You win. Score: \n You: {USER_points} \n CPU: {CPU_points}")
                            exit()
                    else:
                        USER_points += 1
                        print("You gained 1 point, the CPU couldn't play another card")
                        if USER_points > 121:
                            print(f"You win. Score: \n You: {USER_points} \n CPU: {CPU_points}")
                            exit()
                    in_play.clear()
                    count = 0
                    count = play_CPU(count)

            print(f"Here is the current pegging pile \n {in_play}")
            print(f"The count is {count}", end="\n\n")
            # Last card, gains one point if you play it
            if (len(hand_CPU_copy) == 0) and (len(hand_USER_copy) == 0):
                if count == 31:
                    CPU_points += 2
                    print("The CPU played last and made the count 31, they gained 2 points")
                    if CPU_points > 121:
                        print(f"CPU has won. Score: \n CPU: {CPU_points} \n You: {USER_points}")
                        exit()
                else:
                    CPU_points += 1
                    print("The CPU played last, they gained 1 point")
                    if CPU_points > 121:
                        print(f"CPU has won. Score: \n CPU: {CPU_points} \n You: {USER_points}")
                        exit()

                continue

# Scoring, individual hands
def scoring(hand, player):
    if player == "You":
        print("Your hand")
    else:
        print(f"{player} hand")
    print(hand)
    # Last card in hand is the cut card
    def check_RJack(hand):
        cut = hand[-1]
        if cut[0] == 'J':
            return False

        # Is there a Jack
        c1 = hand[0]
        c2 = hand[1]
        c3 = hand[2]
        c4 = hand[3]
        hand_numbers = []
        hand_numbers.append(c1[0])
        hand_numbers.append(c2[0])
        hand_numbers.append(c3[0])
        hand_numbers.append(c4[0])

        jacks = []
        count = 0
        for value in hand_numbers:
            if value == 'J':
                jacks.append(hand[count])
            count += 1

        if len(jacks) == 0:
            return False
    
        # Check suit of jack(s)
        for jack in jacks:
            if jack[-1] == cut[-1]:
                return True
    
        return False
    # Checks for pairs
    def pairs(hand):
        cards = []
        for card in hand:
            if len(card) == 3:
                cards.append("10")
            else:
                cards.append(card[0])

        # Counts appearances of each card
        card_counts = Counter(cards)

        # Initialize results
        result = {
            "pair": False,
            "two_pairs": False,
            "three_of_a_kind": False,
            "four_of_a_kind": False,
            "full_house": False
        }

        # Count the number of pairs and three of a kind
        pair_count = 0
        three_of_a_kind_count = 0

        # Check card counts for patterns
        for value, count in card_counts.items():
            if count == 2:
                pair_count += 1
            elif count == 3:
                three_of_a_kind_count += 1
                result["three_of_a_kind"] = True
            elif count == 4:
                result["four_of_a_kind"] = True

        # Update results based on pair and three of a kind counts
        if pair_count == 1:
            result["pair"] = True
        elif pair_count == 2:
            result["two_pairs"] = True

        # Check for a full house
        if pair_count >= 1 and three_of_a_kind_count >= 1:
            result["full_house"] = True

        return result
    # Checks for groups adding to 15
    def fifteens(hand):
        card_values = []
        for card in hand:
            if len(card) == 3:
                card_values.append(10)
            else:
                n = card[0]
                if n in ltr_cards:
                    n = ltr_cards_dict[n]
                    if n > 10:
                        n = 10
                    card_values.append(n)
                else:
                    card_values.append(int(n))

        # Count groups of cards that sum to 15
        count = 0
        for r in range(2, len(cards) + 1):  # Check all combinations of 2 to 5 cards
            for combo in combinations(card_values, r):
                if sum(combo) == 15:
                    count += 1

        return count
    # Checks for runs
    def c_runs(hand, run_length):
        cards = []
        for card in hand:
            if len(card) == 3:
                cards.append("10")
            else:
                cards.append(card[0])

        # To convert from str to value
        value_map = {
        "A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
        "10": 10, "J": 11, "Q": 12, "K": 13
        }
        card_values = sorted([value_map[card] for card in cards])

        # Find all runs in the hand
        runs = []
        for combo in combinations(card_values, run_length):  # Generate all combinations of "run_length" cards
            if all(combo[i] == combo[i-1] + 1 for i in range(1, len(combo))):  # Check if it's a valid run
                runs.append(list(combo))

        return runs
    # Checks for a flush
    def flush(hand):
        cut = hand[-1]
        hand.remove(cut)
        suits = []

        for card in hand:
            if card[-1] not in suits:
                suits.append(card[-1])
            
        if len(suits) == 1:
            if cut[-1] in suits:
                return 5
            else:
                return 4
        else: 
            return 0

    # Check for right jack
    points = 0
    if check_RJack(hand):
        print(f"{player} had the right jack. +1")
        points += 1
    
    # Check for pairs of any kind
    pair_result = pairs(hand)
    if pair_result["four_of_a_kind"]:
        print(f"{player} had a four of a kind. +12")
        points += 12
    elif pair_result["full_house"]:
        print(f"{player} had a full house. +8")
        points += 8
    elif pair_result["three_of_a_kind"]:
        print(f"{player} had a three of a kind. +6")
        points += 6
    elif pair_result["two_pairs"]:
        print(f"{player} had two pairs. +4")
        points += 4
    elif pair_result["pair"]:
        print(f"{player} had one pair. +2")
        points += 2

    # Check for any combination of 15s
    count_15 = fifteens(hand)
    print(f"{player} had {count_15} groups that add to 15. +{count_15 * 2}")
    points += count_15 * 2

    # Check for runs
    runs5 = c_runs(hand, 5)
    runs4 = c_runs(hand, 4)
    runs3 = c_runs(hand, 3)
    if runs5:
        print(f"{player} had 1 5 card run(s). +5")
        points += 5
    elif runs4:
        print(f"{player} had {len(runs4)} 4 card run(s). +{4 * len(runs4)}")
        points += 4 * len(runs4)
    elif runs3:
        print(f"{player} had {len(runs3)} 3 card run(s). +{3 * len(runs3)}")
        points += 3 * len(runs3)
    
    # Check for flush
    p = flush(hand)
    if p != 0:
        print(f"{player} had a {p} card flush. +{p}")
        points += p

    return points

# Game Begin
USER_crib = start_game(cards)
while USER_points < 121 and CPU_points < 121:

    start_round(cards)
    build_crib()
    cut_card = cut()
    pegging(cut_card)
    hand_CPU.append(cut_card)
    hand_USER.append(cut_card)
    hand_crib.append(cut_card)

    if USER_crib:
        CPU_points += scoring(hand_CPU, "CPU")
        print(f"The CPU now has {CPU_points} points", end="\n\n")
        if CPU_points > 121:
            print("The CPU has won")
            exit()
        hand_CPU.clear()

        USER_points += scoring(hand_USER, "You")
        print(f"You now have {USER_points} points", end="\n\n")
        if USER_points > 121:
            print("You win")
            exit()
        hand_USER.clear()

        USER_points += scoring(hand_crib, "Your crib")
        print(f"You now have {USER_points} points", end="\n\n")
        if USER_points > 121:
            print("You win")
            exit()
        hand_crib.clear()
    
        print(f"Point Totals: \n You: {USER_points} \n CPU: {CPU_points} \n")    
        USER_crib = False
    else:
        USER_points += scoring(hand_USER, "You")
        print(f"You now have {USER_points} points", end="\n\n")
        if USER_points > 121:
            print("You win")
            exit()
        hand_USER.clear()

        CPU_points += scoring(hand_CPU, "CPU")
        print(f"The CPU now has {CPU_points} points", end="\n\n")
        if CPU_points > 121:
            print("The CPU has won")
            exit()
        hand_CPU.clear()
    
        CPU_points += scoring(hand_crib, "CPUs crib")
        print(f"The CPU now has {CPU_points} points", end="\n\n")
        if CPU_points > 121:
            print("The CPU has won")
            exit()
        hand_crib.clear()
    
        print(f"Point Totals: \n You: {USER_points} \n CPU: {CPU_points} \n") 
        USER_crib = True