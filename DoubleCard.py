import numpy as np
import time

class Dir:
    UP, DOWN, LEFT, RIGHT = range(4)


class Cell:
    EMPTY, RED_FILLED, RED_EMPTY, WHITE_FILLED, WHITE_EMPTY, RED, WHITE, FILLED, UNFILLED = range(9)

    @staticmethod
    def color(cell):
        if cell == Cell.EMPTY:
            return Cell.EMPTY

        if cell == Cell.RED_FILLED or cell == Cell.RED_EMPTY:
            return Cell.RED
        else:
            return Cell.WHITE

    @staticmethod
    def fill(cell):
        if cell == Cell.EMPTY:
            return Cell.EMPTY

        if cell == Cell.RED_FILLED or cell == Cell.WHITE_FILLED:
            return Cell.FILLED
        else:
            return Cell.UNFILLED


class Orientation:

    def __init__(self, orientation):

        if orientation % 2 == 0:
            # Vertical card
            dir1 = Dir.UP
            dir2 = Dir.DOWN
        else:
            # Horizontal card
            dir1 = Dir.RIGHT
            dir2 = Dir.LEFT

        # Where cell1 is bottom/left cell and cell2 is top/right cell
        if orientation == 1 or orientation == 4:
            cell1 = Cell.RED_FILLED
            cell2 = Cell.WHITE_EMPTY
        elif orientation == 2 or orientation == 3:
            cell1 = Cell.WHITE_EMPTY
            cell2 = Cell.RED_FILLED
        elif orientation == 6 or orientation == 7:
            cell1 = Cell.WHITE_FILLED
            cell2 = Cell.RED_EMPTY
        else:
            cell1 = Cell.RED_EMPTY
            cell2 = Cell.WHITE_FILLED

        if dir1 == Dir.UP:
            offset = (1, 0)
        else:
            offset = (0, 1)

        self.cell1 = cell1
        self.dir1 = dir1
        self.cell2 = cell2
        self.dir2 = dir2
        self.offset = offset

import BoardDisplay

class Player:
    COLORS, DOTS = False, True


class DoubleCard:

    def __init__(self):

        self.num_rows = 12
        self.num_cols = 8
        self.columns = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8}  # Column label mapping
        self.column_idx_to_letter = 'ABCDEFGH'
        self.turn_number = 0
        self.last_moved_card = None
        self.recycling_mode = False
        self.max_cards_in_game = 24  # The total number of cards split among both players; Affects recycling mode timing
        self.game_over = False
        self.board = np.zeros((self.num_rows, self.num_cols), dtype='3int8')
        self.active_player = False
        self.display = BoardDisplay.BoardDisplay(12, 8, 50)
        self.verbose_output = True  # Set to true if you want to see board state in the console after each move
        self.animate = True  # Set to true if you want to see board build itself when running tests

    def play(self, input_file=None):
        """
        Loops through game states until the game is over
        :return: None
        """
        self.display.start()

        # Initialize players
        if input_file:
            self.active_player = 0
        else:
            self.active_player = int(input("Are you playing for colors(0) or dots(1)\n"))

        # game loop
        while not self.game_over:
            try:
                if input_file:
                    move = input_file.readline().split()
                    # Sleep to give the illusion that the game is animated
                    if self.animate:
                        time.sleep(0.1)
                    # If end of file reached give control back to user
                    if move == []:
                        input_file = None
                        continue
                else:
                    move = input("Enter your move (0 orientation column row)\n").split()
            except:
                print('Error diagonal_open_win.txt invalid')

            self.next_turn(move)
        pass

    def next_turn(self, move):
        """
        Moves the game state to the next turn. Handles switching active players, getting inputs and checking for victory
        :return: None
        """

        # Ensure that the move was valid
        index_offset = 0
        if not self.recycling_mode:
            if len(move) != 4:
                print('incorrect number of parameters, should be 4')
                return
        else:
            index_offset = 3
            if len(move) != 7:
                print('incorrect number of parameters, should be 7')
                return

            # get old coordinate, first cell
            if move[0] not in self.columns:
                print('column value must be between A and H, {} is invalid'.format(move[0]))
                return
            old_col1 = self.columns[move[0]] - 1

            row_val = int(move[1]) - 1
            if row_val > 11 or row_val < 0:
                print('Row value must be between 12 and 1, {} is invalid'.format(row_val + 1))
                return
            old_row1 = row_val

            # get old coordinate, second cell
            if move[2] not in self.columns:
                print('column value must be between A and H, {} is invalid'.format(move[2]))
                return
            old_col2 = self.columns[move[2]] - 1

            row_val = int(move[3]) - 1
            if row_val > 11 or row_val < 0:
                print('Row value must be between 12 and 1, {} is invalid'.format(row_val + 1))
                return
            old_row2 = row_val

        orientation_val = int(move[1 + index_offset])
        if orientation_val < 1 or orientation_val > 8:
            print('Orientation value must be between 1 and 8, {} is invalid'.format(orientation_val))
            return
        orientation = Orientation(orientation_val)

        if move[2 + index_offset] not in self.columns:
            print('column value must be between A and H, {} is invalid'.format(move[2 + index_offset]))
            return
        col = self.columns[move[2 + index_offset]] - 1

        row_val = int(move[3 + index_offset]) - 1
        if row_val > 11 or row_val < 0:
            print('Row value must be between 12 and 1, {} is invalid'.format(row_val + 1))
            return
        row = row_val

        if not self.recycling_mode:
            # play card
            if self.play_card(row, col, orientation):
                print('Played a card at coordinate {}:{}'.format(move[2], row + 1))
                self.turn_number += 1
                # If players have each used up all 12 of their cards, start recycling cards on board
                if self.turn_number >= self.max_cards_in_game:
                    self.recycling_mode = True
            else:
                print('ILLEGAL MOVE')
                return
        else:
            if self.recycle_card(old_row1, old_col1, old_row2, old_col2, row, col, orientation):
                pass

        # Print Board
        self.visualize_board()

        # set next player's turn
        self.active_player = not self.active_player

    def play_card(self, row, col, orientation):
        """
        Plays a card at a given location on the board
        :param row: row where card will be played
        :param col: column where card will be played
        :param orientation: the orientation of the card while being placed
        :return: True if a valid card was played, false otherwise
        """

        if self.valid_move(row, col, orientation, self.board):
                # Place card in the board
                other_row = row + orientation.offset[0]
                other_col = col + orientation.offset[1]
                self.board[row][col] = (orientation.cell1, other_row, other_col)
                self.board[other_row][other_col] = (orientation.cell2, row, col)

                self.display.add_piece(row, col, orientation)

                # Check if this move triggers a victory condition
                if self.victory_move(row, col, self.board) or\
                        self.victory_move(other_row, other_col, self.board):
                    print("Victory condition was met!")
                    self.game_over = True

                return True
        else:
            return False

    def recycle_card(self, old_row1, old_col1, old_row2, old_col2, new_row, new_col, orientation):
        """
        Moves a card from one location to another on the board
        :param old_coord: The coordinate at which the player attempts to take a card
        :param new_coord: The coordinate at which the player attempts to place the card
        :param orientation: the orientation of the card while being placed
        :return: True if a valid card was played, false otherwise
        """

        # validate card removal
        # Ensure the old coordinates correspond to a single card
        if self.board[old_row1][old_col1][1] != old_row2 or self.board[old_row1][old_col1][2] != old_col2:
            print('Old coordinates do not correspond to a single card')
            return False

        # Ensure that cells above card being recycled are empty to allow the move
        if (self.board[old_row2 + 1][old_col2][0] != Cell.EMPTY and old_row2 != old_row1 - 1) or\
                (self.board[old_row1 + 1][old_col1][0] != Cell.EMPTY and old_row1 != old_row2 - 1):
                print('The cells above the old coordinates are occupied. {}:{} and {}:{} cannot be moved since'
                      'otherwise the cards above will float over empty cells'
                      .format(old_row1 + 1, self.column_idx_to_letter[old_col1],
                              old_row1 + 1, self.column_idx_to_letter[old_col1 + 1]))
                return False

        # Ensure that the card is in either a new cord or orientation
        # check coord. of first half
        if (old_row1, old_col1) == (new_row,  new_col):
            # check if in same pos
            if  self.board[old_row1][old_col1][1] == (orientation.offset[0] + new_row) and\
                self.board[old_row1][old_col1][2] == (orientation.offset[1] + new_col):
                print('Cannot recycle card, either coordinate or orientation of card must change')
                return False


        # check if current card is the same as last card played
        if self.last_moved_card == (old_row1, old_col1):
            print('Last card was moved from: {}:{}'.format(old_row1, self.column_idx_to_letter[old_col1]))
            return False

        # store old card values
        old_card_val = [self.board[old_row1][old_col1], self.board[old_row2][old_col2]]

        # testing
        print('old card values: ', old_card_val)

        # set value of old card's location to 0
        self.board[old_row1][old_col1] = 0
        self.board[old_row2][old_col2] = 0
        # play card at new coordinates
        if self.play_card(new_row, new_col, orientation):
            # set old coordinates to 0
            self.last_moved_card = (new_row, new_col)
            self.display.removePiece(old_row1, old_col1)
            return True
        else:
            # error was found recycling card
            # reset old card values
            self.board[old_row1][old_col1] = old_card_val[0]
            self.board[old_row2][old_col2] = old_card_val[1]
            return False

    def valid_move(self, row, col, orientation, board):
        """
        Checks if a card can legally be played at a given location on the board
        :param row: row where card will be played
        :param col: column where card will be played
        :param orientation: the orientation of the card while being placed
        :param board: The board on which to check if the move is valid
        :return: True if the play is valid, false otherwise
        """

        other_row = orientation.offset[0] + row
        other_col = orientation.offset[1] + col

        # Testing
        if self.recycling_mode:
            print('row: {}\n col: {}\n'.format(row,col))

        # Check if card stays within the bounds of the board
        if other_row >= self.num_rows or other_col >= self.num_cols:
            print('Exceeds limits of the board: {}:{}'.format(other_row + 1, self.column_idx_to_letter[other_col]))
            return False

        # Ensure the cells in which the card will be placed are empty
        if board[row][col][0] != Cell.EMPTY or board[other_row][other_col][0] != Cell.EMPTY:
            print('There are already cards at cells: {}:{} or {}:{}'
                  .format(row + 1, self.column_idx_to_letter[col], other_row + 1, self.column_idx_to_letter[other_col]))
            return False

        # Ensure that cells underneath card is not empty
        if row > 0:
            if orientation.dir1 == Dir.RIGHT:
                empty_below = board[row-1][col][0] == Cell.EMPTY or board[row-1][col+1][0] == Cell.EMPTY
                if empty_below:
                    print('Cards cannot float above empty location: {}:{} or {}:{} is empty'
                          .format(row, self.column_idx_to_letter[col], row, self.column_idx_to_letter[col+1]))
                return not empty_below
            else:
                empty_below = board[row-1][col][0] == Cell.EMPTY
                if empty_below:
                    print('Cards cannot float above empty location: {}:{} is empty'
                          .format(row, self.column_idx_to_letter[col]))
                return not empty_below

        # If none of the exit conditions were met, this move is valid
        return True

    def count_streak(self, val, val_checker, row, col, offset, board):
        # Count to the left of the cell for color
        val_streak = 0
        for i in range(1, 4):
            row += offset[0]
            col += offset[1]
            if row >= 0 and row < self.num_rows and col >= 0 and col < self.num_cols:
                if val == val_checker(board[row][col][0]):
                    val_streak += 1
                else:
                    break
            else:
                break

        return val_streak

    def victory_move(self, row, col, board):
        """
        Checks if the placement of the new card triggered a victory
        :param row: row where card will be played
        :param col: column where card will be played
        :param board: The board on which to check if victory has been achieved
        :return: True if the play triggers a victory, false otherwise
        """

        color = Cell.color(board[row][col][0])
        fill = Cell.fill(board[row][col][0])

        # Check vertically
        color_streak = 1
        fill_streak = 1
        color_streak += self.count_streak(color, Cell.color, row, col, (-1, 0), board)
        fill_streak += self.count_streak(fill, Cell.fill, row, col, (-1, 0), board)
        if self.check_victory(color_streak, fill_streak):
            return True

        # Check Horizontal
        color_streak = 1
        fill_streak = 1
        color_streak += self.count_streak(color, Cell.color, row, col, (0, 1), board)
        color_streak += self.count_streak(color, Cell.color, row, col, (0, -1), board)
        fill_streak += self.count_streak(fill, Cell.fill, row, col, (0, 1), board)
        fill_streak += self.count_streak(fill, Cell.fill, row, col, (0, -1), board)
        if self.check_victory(color_streak, fill_streak):
            return True

        # Check Diagonal from bottom left to top right
        color_streak = 1
        fill_streak = 1
        color_streak += self.count_streak(color, Cell.color, row, col, (1, 1), board)
        color_streak += self.count_streak(color, Cell.color, row, col, (-1, -1), board)
        fill_streak += self.count_streak(fill, Cell.fill, row, col, (1, 1), board)
        fill_streak += self.count_streak(fill, Cell.fill, row, col, (-1, -1), board)
        if self.check_victory(color_streak, fill_streak):
            return True

        # Check Diagonal from top left to bottom right
        color_streak = 1
        fill_streak = 1
        color_streak += self.count_streak(color, Cell.color, row, col, (-1, 1), board)
        color_streak += self.count_streak(color, Cell.color, row, col, (1, -1), board)
        fill_streak += self.count_streak(fill, Cell.fill, row, col, (-1, 1), board)
        fill_streak += self.count_streak(fill, Cell.fill, row, col, (1, -1), board)
        if self.check_victory(color_streak, fill_streak):
            return True

        return False

    def check_victory(self, color_streak, fill_streak):
        # Check if victory condition was met
        if color_streak >= 4 and fill_streak >= 4:
            if self.active_player == Player.COLORS:
                print('Colors have won!')
                return True
            else:
                print('Dots have won!')
                return True
        elif color_streak >= 4:
            print('Colors have won!')
            return True
        elif fill_streak >= 4:
            print('Dots have won!')
            return True
        return False

    def visualize_board(self):
        """
        Display the current state of the given board
        :param board: The board to be visualized
        :return: None
        """
        if self.verbose_output:
            print(self.board[::-1, :, 0])


if __name__ == "__main__":
    DoubleCard().play()
