import time
import BoardHelper
from GameConstants import GameConstants
from Cell import Cell
from Card import Card
from Dir import Dir
from BoardState import BoardState
from BoardDisplay import BoardDisplay


class Player:
    COLORS, DOTS = False, True


class DoubleCard:

    def __init__(self):
        self.columns = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8}  # Column label mapping
        self.column_idx_to_letter = 'ABCDEFGH'
        self.state = BoardState()
        self.display = BoardDisplay(GameConstants.NUM_ROWS, GameConstants.NUM_COLS, 50)
        self.verbose_output = True  # Set to true if you want to see board state in the console after each move
        self.animate = True  # Set to true if you want to see board build itself when running tests

        # Initialize the board with empty cells
        for row in range(GameConstants.NUM_ROWS):
            for col in range(GameConstants.NUM_COLS):
                self.state.board[row, col] = Cell((row, col))

    def play(self, input_file=None, exit_after_input=False):
        """
        Loops through game states until the game is over
        :return: None
        """
        if not exit_after_input:
            self.display.start()

        # Initialize players
        if input_file:
            self.state.active_player = 0
        else:
            self.state.active_player = int(input("Are you playing for colors(0) or dots(1)\n"))

        # game loop
        while not self.state.game_over:
            try:
                if input_file:
                    move = input_file.readline().split()
                    # Sleep to give the illusion that the game is animated
                    if self.animate:
                        time.sleep(0.1)
                    # If end of file reached give control back to user
                    if move == []:
                        input_file = None
                        if exit_after_input:
                            break
                        else:
                            continue
                else:
                    move = input("Enter your move (0 orientation column row)\n").split()
            except:
                print('Error diagonal_open_win.txt invalid')

            self.next_turn(move)
        pass

    def validate_input(self, move):
        """
        Makes sure the input is valid
        :return: False if error in input, True otherwise
        """
        if not self.state.recycling_mode:
            #check arg length
            if len(move) != 4:
                print('ERROR: incorrect number of arguments, expected 4 instead of {}'.format(len(move)))
                return False

            # check first arg is 0
            if move[0] != '0':
                print('ERROR: incorrect first argument, expected 0 instead of {}'.format(move[0]))
                return False

            # check for valid orientation
            if not self.is_valid_orientation(move[1]) :
                return False

            # check for valid column
            if not self.is_valid_col(move[2]) :
                return False

            # check for valid row
            if not self.is_valid_row(move[3]) :
                return False

        else:
            # In recycle mode
            if len(move) != 7:
                print('ERROR: incorrect number of arguments, expected 7 instead of {}'.format(len(move)))
                return False

            if not self.is_valid_col(move[0]):
                return False

            if not self.is_valid_row(move[1]):
                return False

            if not self.is_valid_col(move[2]):
                return False

            if not self.is_valid_row(move[3]):
                return False

            if not self.is_valid_orientation(move[4]):
                return False

            if not self.is_valid_col(move[5]):
                return False

            if not self.is_valid_row(move[6]):
                return False
        return True

    def is_valid_row(self, row):
        """
        Checks for valid row
        :return: False if invalid, True otherwise
        """
        if not row.isdigit() or int(row) > GameConstants.NUM_ROWS or int(row) < 1:
            print('ERROR: incorrect orientation, expected number between 1 and 12 instead of {}'.format(row))
            return False
        return True

    def is_valid_col(self, col):
        """
        Checks for valid column
        :return: False if invalid, True otherwise
        """
        if col not in self.columns:
            print('ERROR: column value must be between A and H, {} is invalid'.format(col))
            return False
        return True

    def is_valid_orientation(self, orientation):
        """
        Checks for valid orientation
        :return: False if invalid, True otherwise
        """

        if not orientation.isdigit() or int(orientation) > 8:
            print('ERROR: incorrect orientation, expected number between 1 and 8 instead of {}'.format(orientation))
            return False
        return True


    def next_turn(self, move):
        """
        Moves the game state to the next turn. Handles switching active players, getting inputs and checking for victory
        :return: None
        """

        if self.validate_input(move):

            if not self.state.recycling_mode:
                # play card
                orientation = int(move[1])
                col = self.columns[move[2]] - 1
                row = int(move[3]) - 1
                coord = (row, col)
                card = Card(id=self.state.turn_number, orientation=orientation, coords=coord)

                if self.play_card(card):
                    print('Played a card at coordinate {}:{}'.format(move[2], row + 1))
                    self.state.turn_number += 1
                    # If players have each used up all 12 of their cards, start recycling cards on board
                    if self.state.turn_number >= GameConstants.MAX_CARDS_IN_GAME:
                        self.state.recycling_mode = True
                else:
                    print('ILLEGAL MOVE')
                    return
            else:
                old_col1 = self.columns[move[0]] - 1
                old_row1 = int(move[1]) - 1
                old_col2 = self.columns[move[2]] - 1
                old_row2 = int(move[3]) - 1
                orientation = int(move[4])
                col = self.columns[move[5]] - 1
                row = int(move[6]) - 1
                new_coord = (row, col)
                new_card = Card(id=None, orientation=orientation, coords=new_coord)
                if self.recycle_card((old_row1, old_col1), (old_row2, old_col2), new_card, self.state):
                    print('Played a card at coordinate {}:{}'.format(self.column_idx_to_letter[col], row + 1))

            # Print Board
            self.visualize_board()

            # set next player's turn
            self.state.active_player = not self.state.active_player

    def play_card(self, card, old_coord=None):
        """
        Plays a card at a given location on the board
        :param card: the card while being placed
        :param old_coord: the old coordinates of the card to remove from the board
        :return: True if a valid card was played, false otherwise
        """

        if self.valid_move(card, self.state.board):
                # Place card in the board
                # set board cell values
                BoardHelper.fill_cells(card, self.state)

                if old_coord:
                    self.display.remove_piece(*old_coord)
                self.display.add_piece(self.state.board[card.coords1])

                # Check if this move triggers a victory condition
                if self.victory_move(card.coords1, self.state.board) or\
                        self.victory_move(card.coords2, self.state.board):
                    print("Victory condition was met!")
                    self.state.game_over = True
                # after playing card set last moved card id
                self.state.last_moved_card = card
                return True
        else:
            return False

    def recycle_card(self, coord1, coord2, new_card, state):
        """
        Moves a card from one location to another on the board
        :param coord1: The 1st coordinate at which the player attempts to take a card
        :param coord2: The 2nd coordinate at which the player attempts to take a card
        :param new_card: The coordinate at which the player attempts to place the card
        :return: True if a valid card was played, false otherwise
        """
        new_row, new_col = new_card.coords1

        old_row2 = coord2[0]
        # Ensure that the bottom-left cell is regarded as the first cell of the card
        if coord2[0] < coord1[0] or coord2[1] < coord1[1]:
            temp = coord1
            coord1 = coord2
            coord2 = temp

        # validate card removal
        # Ensure the old coordinates correspond to a single card
        if not state.board[coord1].card or not state.board[coord2].card or \
                state.board[coord1].card.id != state.board[coord2].card.id:
            print('Old coordinates do not correspond to a single card')
            return False

        # get old card
        old_card = state.board[coord1].card
        new_card.id = old_card.id   # Now that you've validated the old card, ensure the new card has same ID

        # Ensure that there is no card above selected card
        above_coord2 = tuple((coord2 + Dir.UP).tolist())
        above_coord1 = tuple((coord1 + Dir.UP).tolist())
        if state.board[above_coord2].card or (state.board[above_coord1].card and old_card.horizontal):
            print('The cells above the old coordinates are occupied. {}:{} and {}:{} cannot be moved since'
                  ' otherwise the cards above will float over empty cells'
                  .format(coord1[0] + 1, self.column_idx_to_letter[coord1[1]],
                          coord1[0] + 1, self.column_idx_to_letter[coord1[1] + 1]))
            return False

        # Ensure that the card is in either a new coord or orientation
        # check coord. of first half
        if old_card.orientation == new_card.orientation and old_card.coords1 == new_card.coords1:
            print('Cannot recycle card, either coordinate or orientation of card must change')
            return False

        # check if current card is the same as last card played
        if self.state.last_moved_card.id == old_card.id:
            print('Last card was moved from: {}:{}, you cannot move this card again this turn'
                  .format(coord1[0], self.column_idx_to_letter[coord1[1]]))
            return False

        # set value of old card's location to Empty
        state.board[coord1].clear()
        state.board[coord2].clear()
        # Decrement highest empty cell values
        if old_card.horizontal:
            state.top_empty_cell[old_card.coords1[1]] -= 1
            state.top_empty_cell[old_card.coords2[1]] -= 1
        else:
            state.top_empty_cell[old_card.coords1[1]] -= 2

        # play card at new coordinates
        if self.play_card(new_card, old_card.coords1):
            # set last moved card
            self.state.last_moved_card = new_card
            return True
        else:
            # error was found recycling card
            # Place the old card back in place
            BoardHelper.fill_cells(old_card, state)
            return False

    def valid_move(self, card, board):
        """
        Checks if a card can legally be played at a given location on the board
        :param card: the card being placed
        :param board: The board on which to check if the move is valid
        :return: True if the play is valid, false otherwise
        """
        row, col = card.coords1
        other_row, other_col = card.coords2

        # Check if card stays within the bounds of the board
        if card.coords2[0] >= GameConstants.NUM_ROWS or card.coords2[1] >= GameConstants.NUM_COLS:
            print('Exceeds limits of the board: {}:{}'.format(card.coords2[0] + 1, self.column_idx_to_letter[card.coords2[1]]))
            return False

        # Ensure the cells in which the card will be placed are empty
        if board[card.coords1].card or board[card.coords2].card:
            print('There are already cards at cells: {}:{} or {}:{}'
                  .format(row + 1, self.column_idx_to_letter[col], other_row + 1, self.column_idx_to_letter[other_col]))
            return False

        # Ensure that cells underneath card is not empty
        if row > 0:
            if card.horizontal:
                empty_below = not board[row-1][col].card or not board[row-1][col+1].card
                if empty_below:
                    print('Cards cannot float above empty location: {}:{} or {}:{} is empty'
                          .format(row, self.column_idx_to_letter[col], row, self.column_idx_to_letter[col+1]))
                return not empty_below
            else:
                empty_below = not board[row-1][col].card
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
            if 0 <= row < GameConstants.NUM_ROWS and 0 <= col < GameConstants.NUM_COLS:
                if val == val_checker(board[row, col]):
                    val_streak += 1
                else:
                    break
            else:
                break

        return val_streak

    def victory_move(self, coord, board):
        """
        Checks if the placement of the new card triggered a victory
        :param card: the card being placed
        :param board: The board on which to check if victory has been achieved
        :return: True if the play triggers a victory, false otherwise
        """

        row, col = coord

        color = board[coord].color
        fill = board[coord].fill

        # Check vertically
        color_streak = 1
        fill_streak = 1
        color_streak += self.count_streak(color, Cell.get_color, row, col, (-1, 0), board)
        fill_streak += self.count_streak(fill, Cell.get_fill, row, col, (-1, 0), board)
        if self.check_victory(color_streak, fill_streak):
            return True

        # Check Horizontal
        color_streak = 1
        fill_streak = 1
        color_streak += self.count_streak(color, Cell.get_color, row, col, (0, 1), board)
        color_streak += self.count_streak(color, Cell.get_color, row, col, (0, -1), board)
        fill_streak += self.count_streak(fill, Cell.get_fill, row, col, (0, 1), board)
        fill_streak += self.count_streak(fill, Cell.get_fill, row, col, (0, -1), board)

        if self.check_victory(color_streak, fill_streak):
            return True

        # Check Diagonal from bottom left to top right
        color_streak = 1
        fill_streak = 1
        color_streak += self.count_streak(color, Cell.get_color, row, col, (1, 1), board)
        color_streak += self.count_streak(color, Cell.get_color, row, col, (-1, -1), board)
        fill_streak += self.count_streak(fill, Cell.get_fill, row, col, (1, 1), board)
        fill_streak += self.count_streak(fill, Cell.get_fill, row, col, (-1, -1), board)
        if self.check_victory(color_streak, fill_streak):
            return True

        # Check Diagonal from top left to bottom right
        color_streak = 1
        fill_streak = 1
        color_streak += self.count_streak(color, Cell.get_color, row, col, (-1, 1), board)
        color_streak += self.count_streak(color, Cell.get_color, row, col, (1, -1), board)
        fill_streak += self.count_streak(fill, Cell.get_fill, row, col, (-1, 1), board)
        fill_streak += self.count_streak(fill, Cell.get_fill, row, col, (1, -1), board)
        if self.check_victory(color_streak, fill_streak):
            return True

        return False

    def check_victory(self, color_streak, fill_streak):
        # Check if victory condition was met
        if color_streak >= 4 and fill_streak >= 4:
            if self.state.active_player == Player.COLORS:
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
            # print(self.state.board[::-1, :, 0])
            pass


if __name__ == "__main__":
    DoubleCard().play()
