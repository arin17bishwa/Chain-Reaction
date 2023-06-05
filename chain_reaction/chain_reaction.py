import random
import sys
from collections import deque
from time import sleep
from typing import Tuple, List, Optional, Union

random.seed(32)


class Cell:
    def __init__(self, balls: int = 0, pos: Tuple[int, int] = (0, 0), max_lim: int = 1, col: int = 0, *args, **kwargs):
        self.pos: Tuple[int, int] = pos
        self.balls: int = balls
        self.max_limit: int = max_lim
        self.color: int = col

    def __repr__(self):
        if self.color == -1:
            return ' ' * 4
        return '{:^4}'.format(str(self.color) * self.balls)

    def __str__(self):
        return self.__repr__()
        # return "Balls->{}; Position->{}; Limit->{}; Color->{}".format(self.balls, self.pos, self.max_limit, self.color)


class GameBoard:
    def __init__(self, board_length: int = 10, num_players: int = 2, *args, **kwargs):
        self.board_length: int = board_length
        self.board: List[List[Cell]] = [
            [
                Cell(
                    balls=0,
                    pos=(i, j),
                    max_lim=self._max_balls(i, j),
                    col=-1
                ) for j in range(board_length)
            ]
            for i in range(board_length)
        ]

        self.num_players: int = num_players
        self._turn_number: int = 1
        self.current_player: int = 0
        self.player_references: dict = {}

    def _is_valid_position(self, x: int, y: int) -> bool:
        return 0 <= x < self.board_length and 0 <= y < self.board_length

    def _max_balls(self, x: int, y: int) -> int:
        if not self._is_valid_position(x, y):
            raise ValueError("Given co-ordinates ({},{}) are outside of the board.".format(x, y))
        if x in (0, self.board_length - 1) or y in (0, self.board_length - 1):
            if x in (0, self.board_length - 1) and y in (0, self.board_length - 1):
                return 1
            return 2
        return 3

    def _get_neighbours(self, x: int, y: int) -> list:
        return [(x + i, y + j) for i, j in ((0, 1), (1, 0), (-1, 0), (0, -1)) if self._is_valid_position(x + i, y + j)]

    def print(self):
        n = self.board_length
        for i in range(n):
            print('-----' * self.board_length + '-')
            for j in range(n):
                print('|' + str(self.board[i][j]), end='')
            print('|')
        print('-----' * self.board_length + '-')

    def emulate_tap(self, x: int, y: int, color: int, _tap: bool = True) -> int:
        if not self._is_valid_position(x, y):
            raise ValueError("Given co-ordinates ({},{}) are outside of the board.".format(x, y))
        curr_cell = self.board[x][y]
        if curr_cell.color not in (-1, color) and _tap:
            print("Invalid move.")
            return 0
        self._expand(x, y, color)
        return 1

    def _expand(self, x: int, y: int, col: int):
        d = deque([self.board[x][y]])
        while d:
            curr_cell = d.popleft()
            curr_cell.color = col
            curr_cell.balls = (curr_cell.balls + 1) % (curr_cell.max_limit + 1)

            # if cell exploded
            if curr_cell.balls == 0:
                curr_cell.color = -1
                for i, j in self._get_neighbours(*curr_cell.pos):
                    d.append(self.board[i][j])
            else:
                curr_cell.color = col

    def bfs(self, x: int, y: int):
        pass


def main():
    n = 3
    p = 2
    board = GameBoard(board_length=n, num_players=p)
    curr_player = 0
    board.print()
    while 1:
        move = list(map(lambda x: int(x) - 1, input(f"Move for player {curr_player + 1}: ").split()))
        success = board.emulate_tap(*move, curr_player)
        if not success:
            continue
        board.print()
        curr_player = (curr_player + 1) % p


if __name__ == '__main__':
    main()
