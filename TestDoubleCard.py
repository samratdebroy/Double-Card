from DoubleCard import DoubleCard
from GameConstants import GameConstants
import BoardDisplay
import AIPlayer
import heuristics


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


def test6():
    with open('test_cases/test_heuristic.txt') as f:
        game = DoubleCard()
        game.verbose_output = False
        game.play(input_file=f, exit_after_input=True)
        next_states = AIPlayer.generate_next_board_states(game.state)
        for i, state in enumerate(next_states):
            print("state {} heuristic val {}".format(i, heuristics.competition_heuristic(state)))
        print('Generated {0} states'.format(len(next_states)))
        display = BoardDisplay.BoardDisplay(GameConstants.NUM_ROWS, GameConstants.NUM_COLS, 50, next_states)
        display.start()
        display.join()


def test7():
    with open('test_cases/test_heuristic2.txt') as f:
        game = DoubleCard()
        game.verbose_output = False
        game.play(input_file=f, exit_after_input=True)
        next_states = AIPlayer.generate_next_board_states(game.state)
        for i, state in enumerate(next_states):
            print("state {} heuristic val {}".format(i, heuristics.competition_heuristic(state)))
        print('Generated {0} states'.format(len(next_states)))
        display = BoardDisplay.BoardDisplay(GameConstants.NUM_ROWS, GameConstants.NUM_COLS, 50, next_states)
        display.start()
        display.join()

def test8():
    with open('test_cases/test_heuristic3.txt') as f:
        game = DoubleCard()
        game.verbose_output = False
        game.play(input_file=f, exit_after_input=True)
        next_states = AIPlayer.generate_next_board_states(game.state)
        for i, state in enumerate(next_states):
            print("state {} heuristic val {}".format(i, heuristics.competition_heuristic(state)))
        print('Generated {0} states'.format(len(next_states)))
        display = BoardDisplay.BoardDisplay(GameConstants.NUM_ROWS, GameConstants.NUM_COLS, 50, next_states)
        display.start()
        display.join()


if __name__ == "__main__":
    print("Starting Test")
    test8()
    print('Testing Over')
