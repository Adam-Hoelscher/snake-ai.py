import sys
import time
from collections import deque
from enum import Enum
from itertools import product
from random import choice

import pygame
from pygame.constants import K_KP_MINUS, K_KP_PLUS

from direction import Direction, Point

DRAW_BUFFER = 2

class Color(pygame.Color, Enum):
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    blue = pygame.Color(0, 0, 255)


class Game(object):

    def __init__(self, size, growth, draw=True):
        self.score = 0
        self.growth = growth
        self.max_score = (size * size - 2) // growth
        # print("making window")
        self.cell_size = 600 // size
        # print("creating board")
        self.size = size
        self.board = set(Point(x, y) for x, y in product(*(2*[range(size)])))
        # print("creating snake")
        self.snake = Snake(Point(size // 2, size // 2), self)
        # print("placing food")
        self.place_food()
        self.moves = 0
        self.tot_play = 0
        self.avg_play = 0
        self.draw = draw
        if draw:
            pygame.init()
            self.window = pygame.display.set_mode(
                (self.cell_size * size, self.cell_size * size))
            self._draw()

    def place_food(self):
        available = set(self.board) - set(self.snake.body)
        if available:
            self.food = choice(list(available))
            return True
        else:
            return False

    def _draw(self):

        self.window.fill(Color.blue)

        if self.food:
            x = self.food.x
            y = self.food.y
            pygame.draw.rect(
                self.window,
                Color.red,
                pygame.Rect(
                    x * self.cell_size + DRAW_BUFFER,
                    y * self.cell_size + DRAW_BUFFER,
                    self.cell_size - 2 * DRAW_BUFFER,
                    self.cell_size - 2 * DRAW_BUFFER)
            )

        body_offset = list(self.snake.body)[1:]
        for idx, (l, r) in enumerate(zip(self.snake.body, body_offset)):
            min_x, max_x = sorted([l.x, r.x])
            min_y, max_y = sorted([l.y, r.y])
            color = Color.green.lerp(Color.white, idx / len(self.snake.body))
            rect = pygame.Rect(
                min_x * self.cell_size + DRAW_BUFFER,
                min_y * self.cell_size + DRAW_BUFFER,
                (max_x - min_x + 1) * self.cell_size - 2 * DRAW_BUFFER,
                (max_y - min_y + 1) * self.cell_size - 2 * DRAW_BUFFER)
            pygame.draw.rect(self.window, color, rect)

        status_str = '; '.join([
            f'Score={self.score:,}',
            f'Moves={self.moves:,}',
            f'Pace={self.avg_play:.6f}'
        ])

        score_font = pygame.font.SysFont('Droid Sans Mono', 32)
        score_surface = score_font.render(
            status_str,
            True,
            Color.black)

        score_rect = score_surface.get_rect()
        self.window.blit(score_surface, score_rect)

        pygame.display.flip()

    def play(self, player_class):

        # print("Creating player")
        self.player = player_class(self)

        # print("Playing game")
        rest = 0.05
        snake = self.snake
        board = self.board
        win = False

        while True:
            if self.draw:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key in (pygame.K_PLUS, pygame.K_KP_PLUS):
                            rest -= .05
                            if rest < 0:
                                rest = 0
                        if event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                            rest += .05

            moves_needed = 1
            while moves_needed:
                safe, new_head, self.score, self.max_score, self.moves, self.tot_play = self._make_move()
                if not safe:
                    return self.score, self.max_score, self.moves, self.tot_play

                if new_head == self.food:
                    self.food = None
                    self.snake.eat()
                    moves_needed += self.growth

                if self.draw:
                    self._draw()
                moves_needed -= 1
                time.sleep(rest)

            if not self.food:
                win = not self.place_food()
                self.score += 1
                print(f'food: {self.food}')

            if win:
                print("WIN!!!")
                return self.score, self.max_score, self.moves, self.tot_play

    def _make_move(self):
        
        snake = self.snake
        board = self.board
        t0 = time.time()
        move = self.player.get_move()
        mv_time = time.time() - t0
        self.moves += 1
        self.tot_play += mv_time
        self.avg_play *= .99
        self.avg_play += .01 * mv_time
        print(f'move {self.moves:,}: {move}: {self.tot_play:.3f}: {self.avg_play:.6f}: {mv_time:.6f}')

        if move is None:
            print("PLAYER FAILED")
            return False, None, self.score, self.max_score, self.moves, self.tot_play

        safe, new_head = snake.move(move, board.difference(snake.body))

        if not safe:
            print("DIED")

        return safe, new_head, self.score, self.max_score, self.moves, self.tot_play


# class Board(object):

#     def __init__(self, size):
#         self.squares = {x + y*1j: None for x, y in product(*(2*[range(size)]))}

#     def draw(self):
#         pass


class Snake(object):

    def __init__(self, head_pos, game):
        body = [
            head_pos,
            head_pos + Direction[0]
        ]
        self.body = deque(body)
        self.growth = 0
        self.game = game
        print(f'snake: {body}')

    def move(self, direction, open):
        if self.growth:
            self.growth -= 1
        else:
            open.add(self.body.pop())
        
        head = self.body[0]
        new_head = head + direction
        self.body.appendleft(new_head)

        return new_head in open, new_head

    def eat(self):
        self.growth += self.game.growth


# class Food(object):

#     def __init__(self, board, snake):
#         available = set(board.squares) - set(snake.body)
#         self.location = choice(available)


# def double_check(player, snake):
#     all_moves = sum((list(x) for x in player.paths), [])
#     head = snake.body[0]
#     history = [head]
#     for mv in all_moves:
#         head += mv
#         history.append(head)
#         assert head.x in range(20)
#         assert head.y in range(20)
