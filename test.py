from game import CribbageGame

def main():
    game = CribbageGame()

    def log(title, state):
        print(f"\n=== {title} ===")
        for k, v in state.items():
            print(k, ":", v)

    print("STATE:", game.state)

    state = game.step()   # START → DEAL
    log("After START → DEAL", state)

    print("USER HAND:", game.hand_user)
    print("CPU HAND:", game.hand_cpu)

    state = game.step()   # DEAL → DISCARD
    log("After DEAL → DISCARD", state)

    game.cpu_discard()
    state = game.user_discard([0, 3])
    log("After DISCARD", state)

    state = game.cut()
    log("After CUT", state)

if __name__ == "__main__":
    main()