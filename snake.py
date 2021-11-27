from game import Game
import random
import player
import argparse

parser = argparse.ArgumentParser(description='Play snake.')
parser.add_argument('--size', type=int, nargs='?', default=30)
parser.add_argument('--growth', type=int, nargs='?', default=2)
parser.add_argument('--seed', type=int, nargs='?', default=1)

args = vars(parser.parse_args())

print(args)

random.seed(args.pop('seed'))

game = Game(**args, draw=True)
print(game.play(player.GraphSearchPlayer))
input()

