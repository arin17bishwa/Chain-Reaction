"""
basic check for checking if it handles the ending cycle correctly


Expected:
{
    "winner": 1,
    "ending":{0:13}
}
"""
import time

from chain_reaction.GameBoard import GameBoard


def main():
    sample00 = [
        [1, 1],
        [1, 3],
        [3, 1],
        [3, 3],
        [2, 2],
        [3, 1],
        [1, 2],
        [2, 2],
        [2, 3],
        [1, 2],
        [2, 2],
        [3, 1],
        [1, 2]
    ]

    it = iter(sample00)
    n = 3
    p = 3
    board = GameBoard(board_length=n, num_players=p)
    curr_player = board.next_color_code()
    board.print()
    while not board.finished():
        try:
            # move = list(map(lambda x: int(x) - 1, input(f"Move for player {curr_player + 1}: ").split()))
            move = next(it)
            print(f"Move for player {curr_player + 1}: {move}")
            move = [move[0] - 1, move[1] - 1]
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
            print(f"Winner: {curr_player+1}")
            break
        time.sleep(0.05)


if __name__ == '__main__':
    main()
