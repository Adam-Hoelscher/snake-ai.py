#! /usr/bin/env python

from game import Game
import random
import player
import typer


def main(size: int = typer.Option(30),
         growth: int = typer.Option(2),
         seed=typer.Option(1)):

    random.seed(seed)
    game = Game(size=size, growth=growth, draw=True)
    print(game.play(player.GraphSearchPlayer))
    input()


if __name__ == "__main__":
    typer.run(main)
