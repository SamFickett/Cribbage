# Card Games - "Cribbage"

## Authors
Samuel Fickett

# Project Overview
This project adapts a program that allows the user to play cribbage against the computer
completely within the terminal. The primary objective is to turn the python file into 
a full web app to gain the experience of creating such an application. 

## Progress Day 1 (4-26-2026)

Began moving over the logic, and formatting for web application. 

Changes from Original:
- Game States as opposed to large logic loop
- Removal of global variables
- Removal of input() and print()
    - Debug print() still exist for testing
- Functional as far as the Cut, Pegging/Scoring not implemented yet

## Progress Day 2 (5-10-2026)

Finished rough version of game.py
All tests inside of test.py return as expected

Next:
- Verify Game Logic
- Add CPU "AI" (Decision Logic)

## Progress Day 3 (5-19-2026)

- Created basic CPU AI for both discards and pegging stages
    - Discard logic scores each possible 4 card hand and selects
        the one that nets them the most points, not including cut
        card, or any traditionally "good" pegging cards
    - Pegging logic is much of the same, analyzing each potential
        card selection, and choosing the one that nets them the
        most points.
- Verified and modified slight game logic bugs inside game.py
- Streamlined for UI using "build_state()" upon return calls
- Fixed bug between scoring and pegging in which the lists containing 
    player hands were cleared during pegging, preventing any points 
    being scored in the next stage (apart from in the crib)
- Test runs through test.py (Early driver script)

Next:
- Frontend
- API
