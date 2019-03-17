from Cell import Cell
from GameConstants import GameConstants
from Player import Player
import numpy as np

def fill_cells(card, state):
    board = state.board
    orientation = card.orientation
    # set the cell values for recently played card
    if orientation == 1 or orientation == 4:
        board[card.coords1].color = Cell.RED
        board[card.coords1].fill = Cell.FILLED

        board[card.coords2].color = Cell.WHITE
        board[card.coords2].fill = Cell.OPEN

    elif orientation == 2 or orientation == 3:
        board[card.coords1].color = Cell.WHITE
        board[card.coords1].fill = Cell.OPEN

        board[card.coords2].color = Cell.RED
        board[card.coords2].fill = Cell.FILLED

    elif orientation == 6 or orientation == 7:
        board[card.coords1].color = Cell.WHITE
        board[card.coords1].fill = Cell.FILLED

        board[card.coords2].color = Cell.RED
        board[card.coords2].fill = Cell.OPEN
    else:
        board[card.coords1].color = Cell.RED
        board[card.coords1].fill = Cell.OPEN

        board[card.coords2].color = Cell.WHITE
        board[card.coords2].fill = Cell.FILLED

    board[card.coords1].card = card
    board[card.coords2].card = card
    board[card.coords1].other = board[card.coords2]
    board[card.coords2].other = board[card.coords1]

    #  Update the state of the highest empty cell in the newly occupied columns
    if card.horizontal:
        state.top_empty_cell[card.coords1[1]] = card.coords1[0] + 1
        state.top_empty_cell[card.coords2[1]] = card.coords2[0] + 1
    else:
        state.top_empty_cell[card.coords1[1]] = max(card.coords1[0] + 1, card.coords2[0] + 1)

    state.cards[card.id] = card


def remove_cells(coord1, coord2, state):
    # set the cell values for recently removed card
    state.board[coord1].clear()
    state.board[coord2].clear()

    #  Update the state of the highest empty cell in the newly unoccupied columns
    state.top_empty_cell[coord1[1]] -= 1
    state.top_empty_cell[coord2[1]] -= 1


def victory_move(coord, state):
    """
    Checks if the placement of the new card triggered a victory
    :param coord: The coordinate on the board where the last card was placed that needs to be checked for victory
    :param state: The board state on which to check if victory has been achieved
    :return: True if the play triggers a victory, false otherwise
    """

    row, col = coord
    board = state.board
    color = board[coord].color
    fill = board[coord].fill

    # Check vertically
    color_streak = 1
    fill_streak = 1
    color_streak += count_streak(color, Cell.get_color, row, col, (-1, 0), board)
    fill_streak += count_streak(fill, Cell.get_fill, row, col, (-1, 0), board)
    if check_victory(color_streak, fill_streak, state):
        return True

    # Check Horizontal
    color_streak = 1
    fill_streak = 1
    color_streak += count_streak(color, Cell.get_color, row, col, (0, 1), board)
    color_streak += count_streak(color, Cell.get_color, row, col, (0, -1), board)
    fill_streak += count_streak(fill, Cell.get_fill, row, col, (0, 1), board)
    fill_streak += count_streak(fill, Cell.get_fill, row, col, (0, -1), board)

    if check_victory(color_streak, fill_streak, state):
        return True

    # Check Diagonal from bottom left to top right
    color_streak = 1
    fill_streak = 1
    color_streak += count_streak(color, Cell.get_color, row, col, (1, 1), board)
    color_streak += count_streak(color, Cell.get_color, row, col, (-1, -1), board)
    fill_streak += count_streak(fill, Cell.get_fill, row, col, (1, 1), board)
    fill_streak += count_streak(fill, Cell.get_fill, row, col, (-1, -1), board)
    if check_victory(color_streak, fill_streak, state):
        return True

    # Check Diagonal from top left to bottom right
    color_streak = 1
    fill_streak = 1
    color_streak += count_streak(color, Cell.get_color, row, col, (-1, 1), board)
    color_streak += count_streak(color, Cell.get_color, row, col, (1, -1), board)
    fill_streak += count_streak(fill, Cell.get_fill, row, col, (-1, 1), board)
    fill_streak += count_streak(fill, Cell.get_fill, row, col, (1, -1), board)
    if check_victory(color_streak, fill_streak, state):
        return True

    return False


def check_victory(color_streak, fill_streak, state):
    # Check if victory condition was met
    if color_streak >= 4 or fill_streak >= 4:
        state.game_over = True

    if color_streak >= 4 and fill_streak >= 4:
        if state.active_player == Player.COLOR_WIN:
            # print('Colors have won!')
            state.winner = Player.COLOR_WIN
            return True
        else:
            # print('Dots have won!')
            state.winner = Player.DOT_WIN
            return True
    elif color_streak >= 4:
        # print('Colors have won!')
        state.winner = Player.COLOR_WIN
        return True
    elif fill_streak >= 4:
        # print('Dots have won!')
        state.winner = Player.DOT_WIN
        return True
    return False


def count_streak(val, val_checker, row, col, dir, board):
    # Count in the direction of dir of the cell for val_checker (color or fill)
    val_streak = 0
    for i in range(1, 4):
        row += dir[0]
        col += dir[1]
        if 0 <= row < GameConstants.NUM_ROWS and 0 <= col < GameConstants.NUM_COLS:
            if val == val_checker(board[row, col]):
                val_streak += 1
            else:
                break
        else:
            break

    return val_streak


def count_streaks_along_line(val_checker, row, col, dir, board):
    streak_list = []

    while row < GameConstants.NUM_ROWS and col < GameConstants.NUM_COLS and row >= 0 and col >= 0:
            # Count the number of continuous values along this line
            val = val_checker(board[row, col])
            if val and val != Cell.EMPTY:
                streak_count = 1 + count_streak(val, val_checker, row, col, dir, board)
                streak_list.append(streak_count)
            else:
                streak_count = 1

            row += dir[0] * streak_count
            col += dir[1] * streak_count

    return streak_list

def within_bounds(row, col):
    if row >= GameConstants.NUM_ROWS or col >= GameConstants.NUM_COLS or row < 0 or col < 0:
        return False
    return  True

def count_open_streaks_along_line(val_checker, row, col, dir, board):
    streak_list = []

    while within_bounds(row, col):
            # Count the number of continuous values along this line
            val = val_checker(board[row, col])
            if val and val != Cell.EMPTY:
                streak_count = 1 + count_streak(val, val_checker, row, col, dir, board)

                # Ensure either end of this streak is empty
                prev_coord = np.array((row, col)) - dir
                next_coord = np.array((row, col)) + dir
                if streak_count >= 4 \
                        or (within_bounds(next_coord[0], next_coord[1]) and not val_checker(board[next_coord[0], next_coord[1]]))\
                        or (within_bounds(prev_coord[0], prev_coord[1]) and not val_checker(board[prev_coord[0], prev_coord[1]])):
                    streak_list.append(streak_count)
            else:
                streak_count = 1

            row += dir[0] * streak_count
            col += dir[1] * streak_count

    return streak_list
