from collections import deque
from copy import deepcopy
from itertools import zip_longest
from game import Game
from direction import Direction, Point
from rle import rle
from search import a_star, make_space
from z3 import Solver, EnumSort, Var, Implies, Or, Array, Datatype, IntSort

FEED = 0
PANIC = 1
LOOP = 2
SLOW_AT = float('inf')
SUICIDE_CHECK = False


class SolverPlayer(object):

    def __init__(self, game: Game):
        self.game = game

    def get_move(self):
        pass

    def _solve_for_path(self):

        solver = Solver()
        mx_moves = self.game.size**2

        PointSort = Datatype("Point")
        PointSort.declare("mk_point", ("x", IntSort()), ("y", IntSort()))
        # PointSort = PointSort.create()

        BodySort = Datatype("Body")
        BodySort.decalre("mk_body", ())

        # MoveSort, (up, right, down, left) = EnumSort("Move", Direction)

        # MoveList = Array("MoveList", MoveSort)
        # # BodyList = Array("BodyList", Point)

        # for mv1, mv2 in zip(MoveList, MoveList[1:]):
        #     solver.Add(Implies(mv1 is None, mv2 is None))

        # curr_body = list(self.game.body)
        # for mv, next_body in zip(MoveList, BodyList):
        #     solver.Add(Or(mv is None, self._check_move_legal(curr_body, mv)))
        #     solver.Add(Or(mv is None, self._make_move(
        #         curr_body, mv) == next_body))

    @classmethod
    def _make_move(body, move):
        head, *mid, _ = body
        next_head = head + move
        return [next_head, head] + mid

    @classmethod
    def _check_move_legal(body, move) -> bool:
        head, *mid, _ = body
        next_head = head + move
        return next_head not in mid
