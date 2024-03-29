import string
from collections import deque
from itertools import chain
from typing import List, Tuple, Generator

from chain_reaction.Cell import Cell


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
        self.active_players = {i: 0 for i in range(num_players)}
        self.next_color_code_gen: Generator[int, int, None] = self._next_color_code()
        self._finished: bool = False
        _header_base_str=' + |'+"{:^4}|"*self.board_length
        self._header:str=_header_base_str.format(*string.ascii_uppercase[:self.board_length])


    def _next_color_code(self) -> Generator[int, int, None]:
        """this is an infinite generator"""
        first_pass:bool=True
        while len(self.active_players) > 1:
            for active_color_code, ball_cnt in self.active_players.items():
                # skip player when their ball count is 0, and it isn't their first turn
                # i.e, they got eliminated
                if (not first_pass) and ball_cnt == 0:
                    continue
                yield active_color_code
                if self._finished:
                    break
            _ = self._pop_inactive_players()
            first_pass = False
        # when only 1 player remains, return that color code only
        while 1:
            yield next(iter(self.active_players))

    def next_color_code(self) -> int:
        return next(self.next_color_code_gen)

    def _pop_inactive_players(self) -> int:
        defeated_color_codes = [color_code for color_code, count in self.active_players.items() if count == 0]
        for defeated_color_code in defeated_color_codes:
            self.active_players.pop(defeated_color_code)
        return len(defeated_color_codes)

    def _check_game_finished(self) -> bool:
        if self._finished:
            return True
        # check for actual finishing
        if len(self.active_players) == 1:
            self._finished = True
        if sum(cnt > 0 for cnt in self.active_players.values()) == 1 \
                and sum(self.active_players.values()) > self.num_players:
            # when only 1 player has non-zero balls and winner has > num_players balls
            self._finished = True
        return self._finished

    def _is_valid_position(self, x: int, y: int) -> bool:
        return 0 <= x < self.board_length and 0 <= y < self.board_length

    def is_valid_move(self, move:Tuple[int,int], color_code:int)->bool:
        if not self._is_valid_position(*move):
            print(f"Invalid move. Given co-ordinates ({move[0]+1},{move[1]+1}) are outside of the board.")
            return False
        x,y=move
        if self.board[x][y].color_code not in (color_code, -1):
            print("Invalid move. Cell already occupied by opponent.")
            return False
        return True

    def _max_balls(self, x: int, y: int) -> int:
        if not self._is_valid_position(x, y):
            raise ValueError("Given co-ordinates ({},{}) are outside of the board.".format(x, y))
        if x in (0, self.board_length - 1) or y in (0, self.board_length - 1):
            if x in (0, self.board_length - 1) and y in (0, self.board_length - 1):
                return 1
            return 2
        return 3

    def _get_neighbours(self, x: int, y: int) -> List[Tuple[int,int]]:
        return [(x + i, y + j) for i, j in ((0, 1), (1, 0), (-1, 0), (0, -1)) if self._is_valid_position(x + i, y + j)]

    def print(self)->None:
        # print(self.active_players)
        print(self._header)
        row_header_iterator = iter(string.ascii_uppercase[:self.board_length])
        for i in range(self.board_length):
            print(('=' if i==0 else '-') * (5 * self.board_length + 4))

            _row_base_str=f" {next(row_header_iterator)} |"+'{}|'*self.board_length
            print(_row_base_str.format(*self.board[i]))

        print('-' * (5 * self.board_length + 4))

    def emulate_tap(self, x: int, y: int, color: int, _tap: bool = True) -> bool:
        valid_move=self.is_valid_move(move=(x,y), color_code=color)
        if not valid_move:
            return False
        self.active_players[color] += _tap
        self._expand(x, y, color)

        return True

    def _expand(self, x: int, y: int, new_color_code: int)->None:
        d = deque([self.board[x][y]])
        while d:
            if self._check_game_finished():
                self._pop_inactive_players()
                return

            # print('+' * 60)
            # print(self.active_players)
            # print('+' * 60)

            curr_cell = d.popleft()
            if curr_cell.color_code != new_color_code and curr_cell.color_code != -1:
                self.active_players[new_color_code] += curr_cell.balls
                self.active_players[curr_cell.color_code] -= curr_cell.balls

            curr_cell.color_code = new_color_code
            curr_cell.balls = (curr_cell.balls + 1) % (curr_cell.max_limit + 1)

            # if cell exploded
            if curr_cell.balls == 0:
                curr_cell.color_code = -1
                for i, j in self._get_neighbours(*curr_cell.pos):
                    d.append(self.board[i][j])
            else:
                curr_cell.color_code = new_color_code
            # time.sleep(0.1)

    def get_empty_cells(self) -> List[Tuple[int, int]]:
        return [cell.pos for cell in chain(*self.board) if cell.balls == 0]

    def get_feasible_cells(self, color_code: int) -> List[Tuple[int, int]]:
        return self.get_empty_cells() + [cell.pos for cell in chain(*self.board) if cell.color_code == color_code]

    def finished(self) -> bool:
        return self._finished
