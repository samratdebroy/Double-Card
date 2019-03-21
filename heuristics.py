from GameConstants import GameConstants
from Cell import Cell
from Dir import Dir
import BoardHelper
import random

def demo_heuristic(state):
    """
    calculates a heuristic value given the board state
    :param state: BoardState object
    """

    # for professor's heuristic
    # loop through cards list and sum according to specs
    board_sum = 0
    coord = lambda c: c.coordinate[0] * GameConstants.NUM_COLS + c.coordinate[1]
    for card in state.cards.values():
        card_cells = [state.board[card.coords1], state.board[card.coords2]]
        for cell in card_cells:
            if cell.color == Cell.WHITE and cell.fill == Cell.OPEN:
                board_sum += coord(cell)

            elif cell.color == Cell.WHITE and cell.fill == Cell.FILLED:
                board_sum += 3 * (coord(cell))

            elif cell.color == Cell.RED and cell.fill == Cell.FILLED:
                board_sum -= 2 * (coord(cell))

            elif cell.color == Cell.RED and cell.fill == Cell.OPEN:
                board_sum -= 1.5 * (coord(cell))
    return board_sum


def competition_heuristic(state):
    """
    calculates a heuristic value given the board state
    :param state: BoardState object
    """

    color_counter = []
    fill_counter = []

    # Check streaks, moving up along first column
    for row in range(0, GameConstants.NUM_ROWS):
        # Check Horizontally
        color_counter.extend(BoardHelper.count_streaks_along_line(Cell.get_color, row, 0, Dir.RIGHT, state.board))
        fill_counter.extend(BoardHelper.count_streaks_along_line(Cell.get_fill, row, 0, Dir.RIGHT, state.board))

        # Check Ascending Diagonals
        color_counter.extend(BoardHelper.count_streaks_along_line(Cell.get_color, row, 0, Dir.DIAG_UR, state.board))
        fill_counter.extend(BoardHelper.count_streaks_along_line(Cell.get_fill, row, 0, Dir.DIAG_UR, state.board))

        # Check Descending Diagonals
        color_counter.extend(BoardHelper.count_streaks_along_line(Cell.get_color, row, 0, Dir.DIAG_DR, state.board))
        fill_counter.extend(BoardHelper.count_streaks_along_line(Cell.get_fill, row, 0, Dir.DIAG_DR, state.board))

    # Check Streaks, moving right along first row
    for col in range(0, GameConstants.NUM_COLS):
        # Check vertical streaks
        color_counter.extend(BoardHelper.count_streaks_along_line(Cell.get_color, 0, col, Dir.UP, state.board))
        fill_counter.extend(BoardHelper.count_streaks_along_line(Cell.get_fill, 0, col, Dir.UP, state.board))

        if col != 0:
            # Check Ascending Diagonals
            color_counter.extend(BoardHelper.count_streaks_along_line(Cell.get_color, 0, col, Dir.DIAG_UR, state.board))
            fill_counter.extend(BoardHelper.count_streaks_along_line(Cell.get_fill, 0, col, Dir.DIAG_UR, state.board))

            # Check Descending Diagonals
            color_counter.extend(BoardHelper.count_streaks_along_line(Cell.get_color, 0, col, Dir.DIAG_DR, state.board))
            fill_counter.extend(BoardHelper.count_streaks_along_line(Cell.get_fill, 0, col, Dir.DIAG_DR, state.board))

    heuristic_val = 0
    heuristic_val += color_counter.count(1) - fill_counter.count(1)
    heuristic_val += (color_counter.count(2) - fill_counter.count(2)) * 3
    heuristic_val += (color_counter.count(3) - fill_counter.count(3)) * 20
    heuristic_val += (color_counter.count(4) - fill_counter.count(4)) * 100000

    return heuristic_val

def random_heuristic(state):
    """
    calculates a heuristic value given the board state
    :param state: BoardState object
    """
    return random.randint(-10000, 10000)


def open_competition_heuristic(state):
    """
    calculates a heuristic value given the board state
    :param state: BoardState object
    """

    color_counter = []
    fill_counter = []

    # Check streaks, moving up along first column
    max_row = max(state.top_empty_cell) - 1

    for row in range(0, GameConstants.NUM_ROWS):

        if row < max_row:
            # Check Horizontally
            color_counter.extend(BoardHelper.count_open_streaks_along_line(Cell.get_color, row, 0, Dir.RIGHT, state.board))
            fill_counter.extend(BoardHelper.count_open_streaks_along_line(Cell.get_fill, row, 0, Dir.RIGHT, state.board))

        # Check Ascending Diagonals
        color_counter.extend(BoardHelper.count_open_streaks_along_line(Cell.get_color, row, 0, Dir.DIAG_UR, state.board))
        fill_counter.extend(BoardHelper.count_open_streaks_along_line(Cell.get_fill, row, 0, Dir.DIAG_UR, state.board))

        # Check Descending Diagonals
        color_counter.extend(BoardHelper.count_open_streaks_along_line(Cell.get_color, row, 0, Dir.DIAG_DR, state.board))
        fill_counter.extend(BoardHelper.count_open_streaks_along_line(Cell.get_fill, row, 0, Dir.DIAG_DR, state.board))

    # Check Streaks, moving right along first row
    for col in range(0, GameConstants.NUM_COLS):
        # Check vertical streaks
        color_counter.extend(BoardHelper.count_open_streaks_along_line(Cell.get_color, 0, col, Dir.UP, state.board))
        fill_counter.extend(BoardHelper.count_open_streaks_along_line(Cell.get_fill, 0, col, Dir.UP, state.board))

        if col != 0:
            # Check Ascending Diagonals
            color_counter.extend(BoardHelper.count_open_streaks_along_line(Cell.get_color, 0, col, Dir.DIAG_UR, state.board))
            fill_counter.extend(BoardHelper.count_open_streaks_along_line(Cell.get_fill, 0, col, Dir.DIAG_UR, state.board))

            # Check Descending Diagonals
            color_counter.extend(BoardHelper.count_open_streaks_along_line(Cell.get_color, 0, col, Dir.DIAG_DR, state.board))
            fill_counter.extend(BoardHelper.count_open_streaks_along_line(Cell.get_fill, 0, col, Dir.DIAG_DR, state.board))

    heuristic_val = 0
    heuristic_val += color_counter.count(1) - fill_counter.count(1)
    heuristic_val += (color_counter.count(2) - fill_counter.count(2)) * 30
    heuristic_val += (color_counter.count(3) - fill_counter.count(3)) * 200000
    heuristic_val += (color_counter.count(4) - fill_counter.count(4)) * 100000000000

    return heuristic_val

def test_heuristic(state):
    """
    Test heuristic using streaks
    """

    color_streak_counter = [0]*4
    fill_streak_counter = [0]*4
    color_streak = 1
    fill_streak = 1
    heuristic_val = 0

    max_row = max(state.top_empty_cell) - 1

    # check horizontal
    for row in range(0, max_row):
        color_streak = 1
        fill_streak = 1
        for col in range(0, GameConstants.NUM_COLS-1):
            if state.board[row][col].color != None:
                if state.board[row][col].color == state.board[row][col+1].color:
                    color_streak += 1
                else:
                    if color_streak > 4:
                        color_streak = 4
                    color_streak_counter[color_streak-1] += 1
                    color_streak = 1

                if state.board[row][col].fill == state.board[row][col+1].fill:
                    fill_streak += 1
                else:
                    if fill_streak > 4:
                        fill_streak = 4
                    fill_streak_counter[fill_streak-1] += 1
                    fill_streak = 1
            else:
                fill_streak = 1
                color_streak = 1


    color_streak = 1
    fill_streak = 1
    # check vertical
    for col in range(0, GameConstants.NUM_COLS):
        color_streak = 1
        fill_streak = 1
        for row in range(0, GameConstants.NUM_ROWS-1):
            if state.board[row][col].color != None:
                if state.board[row][col].color == state.board[row+1][col].color:
                    color_streak += 1
                else:
                    if color_streak > 4:
                        color_streak = 4
                    color_streak_counter[color_streak-1] += 1
                    color_streak = 1

                if state.board[row][col].fill == state.board[row+1][col].fill:
                    fill_streak += 1
                else:
                    if fill_streak > 4:
                        fill_streak = 4
                    fill_streak_counter[fill_streak-1] += 1
                    fill_streak = 1
            else:
                fill_streak = 1
                color_streak = 1


    color_weights = [1, 20, 40, 2000]
    fill_weights = [1, 20, 40, 2000]

    for i in range(0, len(color_weights)):
        heuristic_val += color_streak_counter[i] * color_weights[i]
        heuristic_val -= fill_streak_counter[i] * fill_weights[i]

    return heuristic_val