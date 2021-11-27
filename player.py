from collections import deque
from copy import deepcopy
from itertools import zip_longest

from direction import Point
from rle import rle
from search import a_star, make_space

FEED = 0
PANIC = 1
LOOP = 2
SLOW_AT = float('inf')
SUICIDE_CHECK = False
# SLOW_AT = 1828


class GraphSearchPlayer(object):

    def __init__(self, game):
        self.search_order = 0
        self.game = game
        self.regime = PANIC
        self.last_recovery = None
        self.last_food = None
        self.moves = 0
        self.loop_point = set()
        self._set_path([])

    def _add_to_path(self, add_path, position, size):
        curr_path = list(self.path)
        front = curr_path[:position]
        mid = [(m, (self.moves, p)) for p, m in enumerate(add_path)]
        back = curr_path[position+size:]
        self.path = deque(front + mid + back)

    def _check_loop(self):
        body = self.game.snake.body
        head, *_, tail = body
        # print(head, self.last_recovery)
        in_loop = head == self.last_recovery
        if self.path:
            in_loop |= head + next(iter(self.path))[0] == tail
        if in_loop and self.regime != LOOP:
            self.regime = LOOP
        elif in_loop:
            key = tuple(body)
            if key in self.loop_point:
                self.path.clear()
            self.loop_point.add(key)

        # elif in_loop and not self._gravity():

    def _check_panic(self):
        time_to_panic = self.game.food != self.last_food
        return time_to_panic

    def _gravity(self):
        # return
        board = self.game.board
        body = self.game.snake.body
        food = self.game.food

        mid = self.game.size / 2
        # center = Point(mid, mid)

        path = self._get_path()
        head, *_, tail = body

        open = board.difference(body).difference([food])

        for idx, mv0 in enumerate(path):
            head += mv0
            if head in open:
                open.remove(head)

        head, *_, tail = body
        for idx, (mv0, mv1, mv2) in enumerate(zip(path, path[1:], path[2:])):
            if mv0 != mv1 and mv0 + mv2 != Point(0, 0):
                # keep = head + mv0 + mv1
                change = head + mv0 + mv2
                if change in open and mv0 == mv2:
                    self._add_to_path(
                        # add_path=path[idx+1:idx-1:-1],
                        add_path=[mv2, mv1],
                        position=idx + 1,
                        size=2
                    )
                    return True
            head += mv0
            if head in open:
                open.remove(head)
            # print(idx, head)

        return False

    def _find_paths(self):

        food = self.game.food
        if not food:
            return False

        board = self.game.board
        body = self.game.snake.body
        head, *_, tail = body
        min_length = self.game.snake.growth + self.game.growth
        direction = self.search_order

        points = [head, food, tail]
        points = points[:direction] + points[direction:]
        a, b, c = points

        open = board.difference(body)
        paths = []

        if first_path := a_star(a, b, open):

            next_open = set(open)

            next_head = a
            for step in first_path:
                next_head += step
                if next_head in next_open:
                    next_open.remove(next_head)

            next_open.add(c)

            if second_path := a_star(b, c, next_open):
                paths = [first_path, second_path]

        else:
            self.search_order = (self.search_order + 1) % 2

        found = False
        if len(paths) == 2:
            paths = paths[:direction] + paths[direction:]
            full_path = sum(paths, [])
            full_path += self._get_body_path(body)
            if len(full_path) >= min_length:
                self._set_path(full_path)
                self.last_food = food
                self.last_recovery = head
                found = True

        # if not found:
        #     open = board.difference(body)
        #     open.remove(food)
        #     open.add(tail)
        #     self._set_path(a_star(head, tail, open))

        return found

    def _food_in_path(self):
        head, *_, tail = self.game.snake.body
        for step in self._get_path():
            head += step
            if head == self.game.food:
                return True
        return False

    def _get_body_path(self, body):
        path = []
        front = list(body)[:-1]
        back = list(body)[1:]
        pairs = zip(back[::-1], front[::-1])
        for src, dst in pairs:
            path.append(dst - src)
        return path

    def _get_path(self):
        return [m for m, _ in self.path]

    def _pad_path(self):
        current_path = self._get_path()
        body = self.game.snake.body

        add_path, idx = make_space(
            src=body[0],
            path=current_path,
            open=self.game.board.difference(body).difference([self.game.food]))

        if add_path:
            self._add_to_path(add_path, idx, 1)

        new_path = self._get_path()
        longer = len(current_path) < len(new_path)

        # print(len(current_path), len(new_path), idx, add_path)

        return longer

    def _set_path(self, path):
        self.path = deque((m, (self.moves, p)) for p, m in enumerate(path))

    def _suicidal(self):
        if not SUICIDE_CHECK:
            return False
        my_body = deepcopy(self.game.snake.body)
        my_growth = deepcopy(self.game.snake.growth)
        my_path = deepcopy(self.path)
        my_board = deepcopy(self.game.board)
        while my_path:
            move, calc_time = my_path.popleft()
            open = my_board.difference(my_body)

            # safe, new_head = my_snake.move(move, open)
            if my_growth:
                my_growth -= self.game.growth
            else:
                open.add(my_body.pop())

            head = my_body[0]
            new_head = head + move
            my_body.appendleft(new_head)

            if new_head not in open:
                print("collision at", new_head)
                return True

            open.remove(new_head)

        return False

    def compare_paths(self, path1, path2):
        for p in list(self.game.snake.body)[::-1]:
            print(p)
        head1 = head2 = self.game.snake.body[0]
        for idx, (mv1, mv2) in enumerate(zip_longest(path1, path2)):
            if mv1:
                head1 += mv1[0]
            else:
                head1 = None
            if mv2:
                head2 += mv2[0]
            else:
                head2 = None
            print(idx, head1, head2)

    def _print_path(self):
        for i in enumerate(rle(self._get_path())):
            print(i)

    def get_move(self):

        if self.moves >= SLOW_AT:
            input()

        # check if we're in a loop
        self._check_loop()
        if self.regime == LOOP:
            # print("Not eating. Padding.")

            last_path = deepcopy(self.path)
            if self._pad_path():
                pass
                # print("successfully added 2")
                if self._suicidal():
                    self.compare_paths(last_path, self.path)
                    return None

            last_path = deepcopy(self.path)
            if self._gravity():
                pass
                # print("successfully pulled empty")
                if self._suicidal():
                    self.compare_paths(last_path, self.path)
                    return None

        # check if we should panic
        if self.regime == FEED and self._check_panic():
            # print("PANIC!")
            self.regime = PANIC

        # attempt to stop panic by finding paths
        if self.regime != FEED:
            # print("trying to stop panic")
            last_path = deepcopy(self.path)
            if self._find_paths():
                # print("RECOVER!")
                # print(rle(self._get_path()))
                self.regime = FEED
                if self._suicidal():
                    self.compare_paths(last_path, self.path)
                    return None

        # if self.regime == PANIC:
        #     print("following tail")
        # else:
        #     print("moving to food")

        if self.path:
            move, calc_time = self.path.popleft()
        else:
            move, calc_time = None, 0

        self.path.append((move, calc_time))

        # print(f'move {self.moves}: {move}')
        self.moves += 1

        return move
