from typing import Tuple


class Cell:
    def __init__(self, balls: int = 0, pos: Tuple[int, int] = (0, 0), max_lim: int = 1, col: int = -1, *args, **kwargs):
        self.pos: Tuple[int, int] = pos
        self.balls: int = balls
        self.max_limit: int = max_lim
        self.color_code: int = col

    def __str__(self):
        if self.color_code == -1:
            return ' ' * 4
        return '{:^4}'.format(str(self.color_code) * self.balls)

    def __repr__(self):
        return self.__str__()
