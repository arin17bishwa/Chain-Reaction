from typing import Optional, List, Tuple, Dict
from chain_reaction.GameBoard import GameBoard
class InputParser:
    def __init__(self, num_players:Optional[int]=None,board_size:Optional[int]=None):
        self.num_players:Optional[int]=num_players
        self.board_size:Optional[int]=board_size
        self._game_board:Optional[GameBoard]=None
    @staticmethod
    def get_num_players()->Optional[int]:
        num_players=input('Enter number of players: ')
        if not num_players.isnumeric():
            return
        n=int(num_players)

        return n

    @staticmethod
    def get_board_size()->Optional[int]:
        board_size=input('Enter length of each side of the board(>1 and <27): ')
        if not board_size.isnumeric():
            return
        n=int(board_size)
        if not 1<n<27:
            print("Board size out of range. Enter a valid value.")
            return
        return n

    @staticmethod
    def parse_move(inp:str)->Optional[Tuple[int,int]]:
        """
        permitted move inputs:
        1 5
        A B
        a d
        AT
        ah
        b12
        B12
        13C
        15f
        25 a
        E 5
        """
        def _parse_to_int(ch:str)->int:
            if ch.isnumeric():
                return int(ch)-1
            return ord(ch)-ord('a')

        inp=inp.strip().lower()
        if ' ' in inp:
            inp=inp.split(' ')
            if len(inp)!=2:
                print(f'Please provide the input in a supported format.')
                return
        x=y=None
        if inp[0].isalpha():
            x,y=map(_parse_to_int, (inp[0], inp[1:] if isinstance(inp,str) else inp[-1]))
        elif inp[-1].isalpha():
            x,y=map(_parse_to_int, (inp[:-1] if isinstance(inp,str) else inp[0], inp[-1]))
        else:
            if not isinstance(inp, list):
                print(f"You must specify the position with space separated numbers when using only numbers.")
                return
            x,y=map(_parse_to_int,inp)
        return x,y

    def take_initial_input(self):
        while not self.num_players:
            self.num_players=self.get_num_players()
        while not self.board_size:
            self.board_size=self.get_board_size()

    def validate_move(self, move:Optional[Tuple[int,int]], current_player:int)->bool:
        if move is None:
            return False
        if self.game_board is not None:
            return self.game_board.is_valid_move(move,current_player)
        return self._is_valid_pos(move)

    def _is_valid_pos(self, pos:Tuple[int,int]):
        x,y=pos
        return 0<=x<self.board_size and 0<=y<self.board_size

    def process_move_input(self, current_player:int)->Tuple[int,int]:
        move=None
        while move is None:
            inp=input(f"Move for player {current_player+1}: ")
            _move=self.parse_move(inp)
            if self.validate_move(_move, current_player):
                move=_move
        return move

    @property
    def game_board(self):
        return self._game_board

    @game_board.setter
    def game_board(self, value:GameBoard):
        self._game_board=value


    def get_board_args(self)->Dict[str,int]:
        return {
            'board_length':self.board_size,
            'num_players':self.num_players
        }

    def __str__(self):
        return f"players->{self.num_players} | size->{self.board_size}"
