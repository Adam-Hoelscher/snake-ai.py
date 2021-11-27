from collections import namedtuple
from heapq import heappop, heappush
import numpy as np
import pandas as pd

from direction import Direction, Point

SearchNode = namedtuple("SearchNode", "priority location steps")


def a_star(src, dst, open, heuristic_func=Point.euclid):

    seen = set()
    queue = [SearchNode(0, src, [])]

    while queue:

        _, loc, steps = heappop(queue)

        if loc == dst:
            # yield steps
            return steps

        if loc in seen and steps:
            continue

        seen.add(loc)

        for d in Direction:
            next_loc = loc + d
            if next_loc in open:
                next_steps = steps + [d]
                priority = len(next_steps)
                if heuristic_func:
                    priority += heuristic_func(next_loc, dst)
                entry = SearchNode(priority, next_loc, next_steps)
                heappush(queue, entry)


def dfs(src, dst, open):

    def rf(loc, path, open):
        if loc != src and loc not in open:
            return
        if loc == dst:
            yield path
        else:
            next_open = open.difference([loc])
            for d in Direction:
                next_loc = loc + d
                next_path = path + (d,)
                yield from rf(next_loc, next_path, next_open)

    paths = list(rf(loc=src, path=(), open=open.difference([src])))
    paths.append(())
    return max(paths, key=lambda x: len(x))


def make_space(src, path, open):

    loc = src
    new_open = set(open)
    for step in path:
        loc += step
        if loc in new_open:
            new_open.remove(loc)

    loc = src
    for idx, step in enumerate(path):
        for d in Direction:
            if d == step or d == -step:
                continue
            if (loc + d) in new_open and (loc + d + step) in new_open:
                # winner winner
                return [d, step, -d], idx

        loc += step

    return [], 0
