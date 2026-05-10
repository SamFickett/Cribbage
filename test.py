from game import CribbageGame

def log(title, state):
    print(f"\n=== {title} ===")
    for k, v in state.items():
        print(f"{k}: {v}")

def show_hands(game):
    print("\nUSER:", game.hand_user)
    print("CPU:", game.hand_cpu)
    print("CRIB:", game.hand_crib)

def test_deal_phase(game):
    print("\n\n--- DEAL PHASE TEST ---")
    state = game.step()
    log("START → DEAL", state)
    show_hands(game)

    state = game.step()
    log("DEAL → DISCARD", state)
    return state

def test_discard_phase(game):
    print("\n\n--- DISCARD TEST ---")

    game.cpu_discard()
    state = game.user_discard([0, 3])

    log("After discard", state)
    show_hands(game)
    return state

def test_cut_phase(game):
    print("\n\n--- CUT TEST ---")

    state = game.cut()
    log("CUT RESULT", state)
    return state

def test_pegging_simple(game):
    print("\n\n--- PEGGING TEST (manual plays) ---")

    # Force some simple deterministic plays if possible
    if game.hand_user:
        game.play_user_card(0)

    if game.hand_cpu:
        game.play_cpu_card()

    print("COUNT:", game.count)
    print("IN PLAY:", game.in_play)

def test_full_round(game):
    print("\n\n--- FULL ROUND FLOW ---")

    test_deal_phase(game)
    test_discard_phase(game)
    test_cut_phase(game)

    # simple pegging simulation loop
    for _ in range(10):
        if game.state == "PEGGING":
            if game.current_turn == "USER" and game.hand_user:
                game.play_user_card(0)
            elif game.hand_cpu:
                game.play_cpu_card()
        else:
            break

    print("\nFINAL STATE:", game.state)
    print("USER PTS:", game.user_pts)
    print("CPU PTS:", game.cpu_pts)

def test_scoring_direct(game):
    print("\n\n--- SCORING TEST (forced) ---")

    # force state so we bypass gameplay bugs
    game.cut_card = "7H"
    game.hand_user = ["7D", "7S", "8C", "9C"]
    game.hand_cpu = ["2H", "3H", "4H", "5H"]
    game.hand_crib = ["6D", "6S", "6C", "JD"]

    result = game.score_round()
    print(result)

def main():
    game = CribbageGame()

    print("INITIAL STATE:", game.state)

    # Run modular tests
    test_deal_phase(game)
    test_discard_phase(game)
    test_cut_phase(game)

    # optional deeper tests
    test_pegging_simple(game)

    # hard reset test
    game.reset_round()

    # full simulation
    test_full_round(game)

    # scoring isolation test
    test_scoring_direct(game)

if __name__ == "__main__":
    main()