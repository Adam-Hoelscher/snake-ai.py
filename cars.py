#! /usr/bin/env python

from z3 import (And, Const, Distinct, Implies, IntSort, Length, Or, SeqSort,
                Solver, sat)

from direction import Point


def z3_path(a, b, open):

    # Create the solver
    s = Solver()

    # Infer field size from open set
    size = max(max(pt.x, pt.y) for pt in open)+1

    # Helper so we can use basic ints
    def idx(x, y):
        return x * size + y

    open_idx = [idx(pt.x, pt.y) for pt in open]

    # Points we're using
    xVals = Const("xVals", SeqSort(IntSort()))
    yVals = Const("yVals", SeqSort(IntSort()))
    pairs = Const("pairs", SeqSort(IntSort()))
    pLen = Length(pairs)
    # Constraint 1
    s.add(Length(xVals) == Length(yVals))
    s.add(Length(xVals) == pLen)
    # Constraint 2
    s.add(Distinct(pairs))

    # Constraint 3 Path starts at a, ends at b
    s.add(
        xVals[0] == a.x, yVals[0] == a.y,
        xVals[pLen-1] == b.x, yVals[pLen-1] == b.y,
    )

    for k in range(size**2):

        s.add(Implies(
            k < pLen, And(
                # Constraint 4 Cell inbounds
                0 <= xVals[k], xVals[k] < size,
                0 <= yVals[k], yVals[k] < size,
                # Cells are not repeated Constraint 5
                idx(xVals[k], yVals[k]) == pairs[k],
                # Constraint 6
                *[pairs[k] != pairs[pre] for pre in range(k)],
            )
        ))

        s.add(Implies(
            And(0 < k, k < pLen), And(
                # Contstraint 7 Adjacent indexes are adjacent points
                Or(
                    And(xVals[k-1] == xVals[k]-1, yVals[k-1] == yVals[k]),
                    And(xVals[k-1] == xVals[k]+1, yVals[k-1] == yVals[k]),
                    And(xVals[k-1] == xVals[k], yVals[k-1] == yVals[k]-1),
                    And(xVals[k-1] == xVals[k], yVals[k-1] == yVals[k]+1),
                ),
                # Contstraint 8 The cells we select are open
                Or(pairs[k] == v for v in open_idx)
            )))

    def extract_path(m):
        path = []
        for k in range(m.eval(pLen).as_long()):
            path.append(Point(
                m.eval(xVals[k]).as_long(),
                m.eval(yVals[k]).as_long(),
            ))
        return path

    if s.check() != sat:
        return None

    m = s.model()
    path = extract_path(m)
    steps = [y-x for x, y in zip(path, path[1:])]

    # # Optional: enabling this block makes the snake take a slightly longer path if possible; this may help preventing "dead space" in long games
    # s.add(pLen == m.eval(pLen).as_long()+2) if s.check() == sat: m = s.model()
    # path = extract_path(m) steps = [y-x for x, y in zip(path, path[1:])]

    return steps
