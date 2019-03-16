from GameConstants import GameConstants
from Cell import Cell
from Dir import Dir
import BoardHelper

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

        if col == 0:
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
