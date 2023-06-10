"""
test if the move input parser is working correctly
"""
from chain_reaction.GameBoard import GameBoard
from InputProcessor import InputParser

TC={
    '1 1':(0,0),
    'A B':(0,1),
    'c B':(2,1),
    'D a':(3,0),
    'D F':(3,5),
    'b c':(1,2),
    'ae':(0,4),
    'Ae':(0,4),
    'aE':(0,4),
    'AE':(0,4),
    'a 3':(0,2),
    'A 3':(0,2),
    '4 E':(3,4),
    '4 e':(3,4),
    '1e':(0,4),
    '1E':(0,4),
    '5d':(4,3),
    '5D':(4,3),

    '13':None,

}

def func():
    ip=InputParser(num_players=5, board_size=26)
    board=GameBoard(**ip.get_board_args())
    ip.game_board=board
    success=0
    for key,val in TC.items():
        out=ip.parse_move(key)
        if out!=val:
            print(f"Wrong for: {key} | Expected: {val} | Got: {out}")
        success+=out==val
    print(f'Passed: {success}/{len(TC)}')





def main():
    func()

if __name__ == '__main__':
    main()