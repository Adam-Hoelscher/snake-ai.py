#! /usr/bin/env python

import random

import typer

import pathfinder_player
import solver_player
from game import Game


def main(
        player: str = typer.Option(),
        size: int = typer.Option(6),
        growth: int = typer.Option(2),
        seed=typer.Option(1)):

    random.seed(seed)
    game = Game(size=size, growth=growth, draw=True)
    if player[0].upper() == "P":
        print(game.play(pathfinder_player.GraphSearchPlayer))
    elif player[0].upper() == "Z":
        print(game.play(solver_player.SolverPlayer))
    input()


if __name__ == "__main__":
    typer.run(main)
