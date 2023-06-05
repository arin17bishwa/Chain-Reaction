"""
checks the case where an ineligible user was being asked to make a move.
"""
from chain_reaction.GameBoard import GameBoard
import time, random

random.seed(50)


def main():
    n=5
    p=10
    board = GameBoard(board_length=n, num_players=p)
    curr_player = board.next_color_code()
    board.print()
    while not board.finished():
        try:
            move = random.choice(board.get_feasible_cells(curr_player))
            print(f"Move for player {curr_player}: {move}")
            assert len(move) == 2
        except Exception as e:
            print('Invalid move. Please try with correct input.')
            time.sleep(3)
            continue
        try:
            success = board.emulate_tap(*move, curr_player)
        except ValueError:
            continue
        if not success:
            continue
        board.print()
        curr_player = board.next_color_code()
        if board.finished():
            print(f"Winner: {curr_player}")
            break
        # time.sleep(0.1)


if __name__ == '__main__':
    main()
