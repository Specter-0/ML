from t import Game
import random, sys

game = Game()

if len(sys.argv) < 2 or not sys.argv[1].isdigit():
    print("provide a valid number of birds")
    quit()

bird_count = int(sys.argv[1])

game.setup(bird_count)

while True:
    game.mainloop()
    game.reset(bird_count)