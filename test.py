from game import CribbageGame

game = CribbageGame()

game.step()
game.step()

print("User hand:", game.hand_user)
print("CPU hand:", game.hand_cpu)
print("State:", game.state)