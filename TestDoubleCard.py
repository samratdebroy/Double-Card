from DoubleCard import DoubleCard
from GameConstants import GameConstants
import BoardDisplay
import AIPlayer


def test1():
    with open('test_cases/diagonal_open_win.txt') as f:
        game = DoubleCard()
        game.verbose_output = False
        game.play(input_file=f)


def test2():
    with open('test_cases/24_valid_moves_no_win.txt') as f:
        game = DoubleCard()
        game.verbose_output = False
        game.play(input_file=f)


def test3():
    with open('test_cases/recycle_card_test.txt') as f:
        game = DoubleCard()
        game.verbose_output = False
        game.play(input_file=f)


def test4():
    with open('test_cases/recycle_card_test.txt') as f:
        game = DoubleCard()
        game.verbose_output = False
        game.play(input_file=f, exit_after_input=True)
        next_states = AIPlayer.generate_next_board_states(game.state)
        print('Generated {0} states'.format(len(next_states)))
        display = BoardDisplay.BoardDisplay(GameConstants.NUM_ROWS, GameConstants.NUM_COLS, 50, next_states)
        display.start()
        display.join()


def test5():
    game = DoubleCard()
    next_states = AIPlayer.generate_next_board_states(game.state)
    print('Generated {0} states'.format(len(next_states)))
    display = BoardDisplay.BoardDisplay(GameConstants.NUM_ROWS, GameConstants.NUM_COLS, 50, next_states)
    display.start()
    display.join()


if __name__ == "__main__":
    print("Starting Test")
    test4()
    print('Testing Over')
