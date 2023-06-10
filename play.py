from InputProcessor import InputParser
from chain_reaction.GameBoard import GameBoard


def func()->None:
    ip=InputParser()
    ip.take_initial_input()
    board=GameBoard(**ip.get_board_args())
    ip.game_board=board
    curr_player=board.next_color_code()
    board.print()
    while not board.finished():
        move=ip.process_move_input(current_player=curr_player)
        move_success=board.emulate_tap(*move, color=curr_player)
        if move_success:
            board.print()
            curr_player=board.next_color_code()
    if board.finished():
        print(f"Winner: {curr_player+1}")
def main()->None:
    func()


if __name__ == '__main__':
    main()