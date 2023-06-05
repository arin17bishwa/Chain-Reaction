import time

from GameBoard import GameBoard


def main():
    n = 3
    p = 2
    board = GameBoard(board_length=n, num_players=p)
    curr_player = board.next_color_code()
    board.print()
    while not board.finished():
        try:
            move = list(map(lambda x: int(x) - 1, input(f"Move for player {curr_player + 1}: ").split()))
            print(f"Move for player {curr_player + 1}: {move}")
            assert len(move) == 2
        except AssertionError or ValueError as e:
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


if __name__ == '__main__':
    main()
