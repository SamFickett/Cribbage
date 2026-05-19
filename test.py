from game import CribbageGame

def log(state):
    print("\n------------------------------")
    print("STATE:", state["state"])
    print("TURN:", state.get("turn"))
    print("COUNT:", state.get("count"))
    print("USER PTS:", state.get("user_pts"))
    print("CPU PTS:", state.get("cpu_pts"))
    print("IN PLAY:", state.get("in_play"))
    print("CUT:", state.get("cut_card"))
    print("LAST ACTION:", state.get("last_action"))
    print("LEGAL USER:", state["legal_moves"]["user"])
    print("------------------------------")

def run_step(game):
    state = game.step()
    log(state)
    return state

def play_user_auto(game):
    """Automatically plays first legal card"""
    state = game.build_state()

    legal = state["legal_moves"]["user"]
    if not legal:
        return game.play_user_card(0)  # will trigger GO logic

    return game.play_user_card(legal[0])

def play_cpu_auto(game):
    return game.play_cpu_card()

def run_full_game():
    game = CribbageGame()

    print("\n=== START GAME ===")
    run_step(game)

    print("\n=== DEAL ===")
    run_step(game)

    print("\n=== DISCARD PHASE ===")
    run_step(game)

    # CPU discard first (simple simulation)
    game.cpu_discard()
    log(game.build_state(last_action={"type": "cpu_discard_test"}))

    # USER discard (choose first 2 cards)
    game.user_discard([0, 1])
    log(game.build_state(last_action={"type": "user_discard_test"}))

    print("\n=== CUT ===")
    run_step(game)
    game.cut()
    log(game.build_state(last_action={"type": "cut"}))

    print("\n=== PEGGING ===")

    # Pegging loop
    while game.state == "PEGGING":
        state = game.build_state()

        if game.current_turn == "USER":
            result = play_user_auto(game)
        else:
            result = play_cpu_auto(game)

        log(result)

    print("\n=== PEGGING COMPLETE ===")

    # Force scoring step
    game.state = "SCORING"
    final = run_step(game)

    print("\n=== FINAL RESULT ===")
    log(final)

def run_single_step_debug():
    """Useful for debugging step() only"""
    game = CribbageGame()

    print("\nSTART:")
    run_step(game)

    print("\nDEAL:")
    run_step(game)

    print("\nDISCARD STEP:")
    run_step(game)

if __name__ == "__main__":
    run_full_game()