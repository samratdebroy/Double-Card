import numpy as np


class Dir:
    UP, DOWN, LEFT, RIGHT = range(4)


class Cell:
    EMPTY, RED_FILLED, RED_EMPTY, WHITE_FILLED, WHITE_EMPTY = range(5)


class Orientation:

    def __init__(self, orientation):
        
        if orientation % 2 == 0:
            # Vertical card
            dir1 = Dir.UP
            dir2 = Dir.DOWN
            
            # Whether vertical or horizontal, follows same pattern
            orientation -= 1
        else:
            # Horizontal card
            dir1 = Dir.RIGHT
            dir2 = Dir.LEFT

        if orientation == 1:
            cell1 = Cell.RED_FILLED
            cell2 = Cell.WHITE_EMPTY
        elif orientation == 3:
            cell1 = Cell.WHITE_EMPTY
            cell2 = Cell.RED_FILLED
        elif orientation == 5:
            cell1 = Cell.RED_EMPTY
            cell2 = Cell.WHITE_FILLED
        else:
            cell1 = Cell.WHITE_FILLED
            cell2 = Cell.RED_EMPTY
            
        if dir1 == Dir.UP:
            offset = (1, 0)
        else:
            offset = (0, 1)
            
        self.cell1 = cell1
        self.dir1 = dir1
        self.cell2 = cell2
        self.dir2 = dir2
        self.offset = offset


class Player:
    COLORS, DOTS = False, True


class DoubleCard:

    def __init__(self):

        self.num_rows = 12
        self.num_cols = 8
        self.columns = {'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8}
        self.turn_number = 0
        self.last_moved_card = None
        self.recycling_mode = False
        self.game_over = False
        self.board = np.zeros((self.num_rows, self.num_cols), dtype='2int8')
        self.active_player = False


    def play(self):
        """
        Loops through game states until the game is over
        :return: None
        """

        # Initialize players
        self.active_player = int(input("Are you playing for colors(0) or dots(1)\n"))

        # game loop
        while not self.game_over:
            self.next_turn()
        pass

    def next_turn(self):
        """
        Moves the game state to the next turn. Handles switching active players, getting inputs and checking for victory
        :return: None
        """

        # get move from player
        valid_input = False
        while not valid_input:
                move = input("Enter your move (0 orientation column row)\n").split()
                if not self.recycling_mode:

                    if len(move) != 4:
                        print('incorrect number of parameters, should be 4')
                        continue

                    orientation_val = int(move[1])
                    if orientation_val < 1 or orientation_val > 8:
                        print('Orientation value must be between 1 and 8, {} is invalid'.format(orientation_val))
                        continue    
                    orientation = Orientation(orientation_val)
                    
                    if move[2] not in self.columns:
                        print('column value must be between A and H, {} is invalid'.format(move[2]))
                        continue
                    col = self.columns[move[2]] - 1

                    row_val = int(move[3]) - 1
                    if row_val > 11 or row_val < 0:
                        print('Row value must be between 12 and 1, {} is invalid'.format(row_val))
                        continue
                    row = row_val

                    valid_input = True


        # play card
        if self.play_card(row, col, orientation):
            print('Played a card at coordinate {}:{}'.format(move[2], row))
        else:
            print('ILLEGAL MOVE')
        self.visualize_board()
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

                # Check if this move triggers a victory condition
                if self.victory_move(row, col, orientation, self.board):
                    print("Victory condition was met!")
                    self.game_over = True

                # Place card in the board
                self.board[row][col] = (orientation.cell1, orientation.dir1)
                self.board[row + orientation.offset[0]][col + orientation.offset[1]] =\
                    (orientation.cell2, orientation.dir2)

                return True
        else:
            return False

    def recycle_card(self, old_coord, new_coord, orientation):
        """
        Moves a card from one location to another on the board
        :param old_coord: The coordinate at which the player attempts to take a card
        :param new_coord: The coordinate at which the player attempts to place the card
        :param orientation: the orientation of the card while being placed
        :return: True if a valid card was played, false otherwise
        """
        pass

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

        # at shuffle phase, check if current card is the same as last card played
        if self.last_moved_card == (row, col):
            print('Last card was moved from: {}:{}'.format(row, col))
            return False

        # Check if card stays within the bounds of the board
        if  other_row >= self.num_rows or other_col >= self.num_cols:
            print('Exceeds limits of the board: {}:{}'.format(other_row, other_col))
            return False

        # Ensure the cells in which the card will be placed are empty
        if board[row][col][0] != Cell.EMPTY or board[other_row][other_col][0] != Cell.EMPTY:
            print('There are already cards at cells: {}:{} or {}:{}'.format(row, col, other_row, other_col))
            return False

        # Ensure that cells underneath card is not empty
        if row > 0:
            if orientation.dir1 == Dir.RIGHT:
                print('Cards cannot float above empty location: {}:{} or {}:{}'.format(row-1, col, row-1, col+1))
                return board[row-1][col][0] != Cell.EMPTY and board[row-1][col+1][0] != Cell.EMPTY
            else:
                print('Cards cannot float above empty location: {}:{}'.format(row-1, col))
                return board[row-1][col][0] != Cell.EMPTY

        # If none of the exit conditions were met, this move is valid
        return True

        


    def victory_move(self, row, col, orientation, board):
        """
        Checks if the placement of the new card triggered a victory
        :param row: row where card will be played
        :param col: column where card will be played
        :param orientation: the orientation of the card while being placed
        :param board: The board on which to check if victory has been achieved
        :return: True if the play triggers a victory, false otherwise
        """
        pass

    def visualize_board(self):
        """
        Display the current state of the given board
        :param board: The board to be visualized
        :return: None
        """
        print(self.board[::-1, :, 0])
        pass

if __name__ == "__main__":
    DoubleCard().play()