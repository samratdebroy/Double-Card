import numpy as np
import time

class Dir:
    UP = np.array((1,0))
    DOWN = np.array((-1,0))
    LEFT = np.array((0,-1))
    RIGHT = np.array((0,1))


class Cell:
    EMPTY, RED, WHITE, FILLED, OPEN = range(5)

    def __init__(self, coord):
        self.coordinate = coord # Coordinate of the cell in the board
        self.color = None
        self.fill = None
        self.card = None  # Card object referenced in this cell
        self.other = None # Cell containing the other half of the card

    def clear(self):
        self.color = None
        self.fill = None
        self.card = None  # Card object referenced in this cell
        self.other = None # Cell containing the other half of the card

    @staticmethod
    def get_color(cell):
        return cell.color

    @staticmethod
    def get_fill(cell):
        return cell.fill


class Card:

    def __init__(self, id,  orientation, coords):

        self.id = id
        self.orientation = orientation
        self.horizontal = False
        self.coords1 = coords
        self.coords2 = np.zeros(2)

        if orientation % 2 == 0:
            # Vertical card
            self.horizontal = False
            coord = self.coords1 + Dir.UP
            self.coords2 = tuple(coord.tolist()) # Convert Numpy array to tuple
        else:
            # Horizontal card
            self.horizontal = True
            coord = self.coords1 + Dir.RIGHT
            self.coords2 = tuple(coord.tolist())

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
        self.last_moved_card_id = None
        self.recycling_mode = False
        self.max_cards_in_game = 24  # The total number of cards split among both players; Affects recycling mode timing
        self.game_over = False
        self.board = np.empty((self.num_rows, self.num_cols), dtype=object)
        self.active_player = False
        self.display = BoardDisplay.BoardDisplay(self.num_rows, self.num_cols, 50)
        self.verbose_output = True  # Set to true if you want to see board state in the console after each move
        self.animate = True  # Set to true if you want to see board build itself when running tests

        # Initialize the board with empty cells
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self.board[row, col] = Cell((row, col))

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
            coord = (row, col)
            card = Card(id=self.turn_number, orientation=orientation_val, coords=coord)

            if self.play_card(card):
                print('Played a card at coordinate {}:{}'.format(move[2], row + 1))
                self.turn_number += 1
                # If players have each used up all 12 of their cards, start recycling cards on board
                if self.turn_number >= self.max_cards_in_game:
                    self.recycling_mode = True
            else:
                print('ILLEGAL MOVE')
                return
        else:

            new_coord = (row, col)
            new_card = Card(id=None, orientation=orientation_val, coords=new_coord)
            if self.recycle_card((old_row1, old_col1), (old_row2, old_col2), new_card, self.board):
                pass

        # Print Board
        self.visualize_board()

        # set next player's turn
        self.active_player = not self.active_player

    def play_card(self, card, old_coord=None):
        """
        Plays a card at a given location on the board
        :param card: the card while being placed
        :param old_coord: the old coordinates of the card to remove from the board
        :return: True if a valid card was played, false otherwise
        """

        if self.valid_move(card, self.board):
                # Place card in the board
                # set board cell values
                DoubleCard.fill_cells(card, self.board)

                if old_coord:
                    self.display.removePiece(*old_coord)
                self.display.add_piece(self.board[card.coords1])

                # Check if this move triggers a victory condition
                if self.victory_move(card.coords1, self.board) or\
                        self.victory_move(card.coords2, self.board):
                    print("Victory condition was met!")
                    self.game_over = True

                return True
        else:
            return False

    def recycle_card(self, coord1, coord2, new_card, board):
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
            temp = (coord1[0], coord1[1])
            coord1[0] = coord2[0]
            coord1[1] = coord2[1]
            coord2[0] = temp[0]
            coord2[1] = temp[1]


        # validate card removal
        # Ensure the old coordinates correspond to a single card
        if board[coord1].card.id != board[coord2].card.id:
            print('Old coordinates do not correspond to a single card')
            return False

        # get old card
        old_card = board[coord1].card
        new_card.id = old_card.id   # Now that you've validated the old card, ensure the new card has same ID

        # Ensure that there is no card above selected card
        above_coord2 = tuple((coord2 + Dir.UP).tolist())
        above_coord1 = tuple((coord1 + Dir.UP).tolist())
        if board[above_coord2].card or (board[above_coord1].card and old_card.horizontal):
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
        if self.last_moved_card_id == old_card.id:
            print('Last card was moved from: {}:{}, you cannot move this card again this turn'
                  .format(coord1[0], self.column_idx_to_letter[coord1[1]]))
            return False

        # set value of old card's location to Empty
        board[coord1].clear()
        board[coord2].clear()
        # play card at new coordinates
        if self.play_card(new_card):
            # set last moved card
            self.last_moved_card_id = new_card.id
            return True
        else:
            # error was found recycling card
            # Place the old card back in place
            DoubleCard.fill_cells(old_card, board)
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
        if card.coords2[0] >= self.num_rows or card.coords2[1] >= self.num_cols:
            print('Exceeds limits of the board: {}:{}'.format(card.coords2[0] + 1, self.column_idx_to_letter[card.coords2[1]]))
            return False

        test = board[card.coords1]
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
            if row >= 0 and row < self.num_rows and col >= 0 and col < self.num_cols:
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
            # print(self.board[::-1, :, 0])
            pass

    @staticmethod
    def fill_cells(card, board):

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

if __name__ == "__main__":
    DoubleCard().play()
