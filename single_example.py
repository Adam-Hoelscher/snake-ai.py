#! /usr/bin/env python

from datetime import datetime

from z3 import (And, Const, Datatype, Exists, ForAll, Implies, Ints, IntSort,
                Length, Or, SeqSort, Solver, sat)

from direction import Point

# Inputs for the individual turn come from the <Game> object
body = [Point(1, 2), Point(2, 2), Point(2, 3), Point(2, 4)]
food = Point(3, 4)
size = 5

# Create the solver
s = Solver()

# Z3 datatype to represent points
PointSort = Datatype("PointSort")
PointSort.declare("new", ("x", IntSort()), ("y", IntSort()))
PointSort = PointSort.create()

# Helper functions for constraints


def adjacent(p, q):
    # check if pair of points is manhattan adjacent
    return Or(
        And(
            PointSort.x(p) == PointSort.x(q) + 1,
            PointSort.y(p) == PointSort.y(q)),
        And(
            PointSort.x(p) == PointSort.x(q) - 1,
            PointSort.y(p) == PointSort.y(q)),
        And(
            PointSort.x(p) == PointSort.x(q),
            PointSort.y(p) == PointSort.y(q) + 1),
        And(
            PointSort.x(p) == PointSort.x(q),
            PointSort.y(p) == PointSort.y(q) - 1),
    )


def inbounds(p):
    '''
    Check is point is in on the board
    '''
    return And(
        0 <= PointSort.x(p), PointSort.x(p) < size,
        0 <= PointSort.y(p), PointSort.y(p) < size,
    )


def feed(p):
    return And(
        PointSort.x(p) == food.x,
        PointSort.y(p) == food.y,
    )


Path = Const("Path", SeqSort(PointSort))
pLen = Length(Path)

bLen = len(body)

# Constraints so that we can dovetail with sruvival logic
s.add(pLen > bLen)
for i, pt in enumerate(body):
    j = pLen-bLen+i
    s.add(PointSort.x(Path[j]) == pt.x)
    s.add(PointSort.y(Path[j]) == pt.y)

# Index variables for checking Path
i, j = Ints("i j")
used_path = And(0 <= i, i < pLen, 0 <= j, j < pLen)

# Path inbounds
s.add(ForAll([i], Implies(
    used_path,
    inbounds(Path[i])
)))

# Adjacent indexes are adjacent points
s.add(ForAll([i, j], Implies(
    And(used_path, i+1 == j),
    adjacent(Path[i], Path[j])
)))

# Points are all distinct
s.add(ForAll([i, j], Implies(
    And(0 <= i, i < j, j < pLen),
    Path[i] != Path[j]
)))

# Food must be in the Path
s.add(Exists(i, And(
    used_path,
    feed(Path[i]))))


def extract_points(m):
    points = []
    for k in range(m.eval(pLen).as_long()):
        elem = Path[k]
        points.append(Point(
            m.eval(PointSort.x(elem)).as_long(),
            m.eval(PointSort.y(elem)).as_long(),
        ))
    return points


sol = 0
t = datetime.now()
print("Beg", t)
while s.check() == sat:
    sol += 1
    m = s.model()
    print(sol, datetime.now()-t, extract_points(m))
    s.add(Path != m.eval(m[Path]))
    # break
