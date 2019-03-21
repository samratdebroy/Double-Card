from Player import Player
from GameConstants import GameConstants
from Card import Card
from Dir import Dir
import BoardHelper


class HumanPlayer(Player):

    def __init__(self, winning_token, display):
        Player.__init__(self, winning_token, display)

        self.columns = GameConstants.COLUMNS  # Column label mapping
        self.column_idx_to_letter = GameConstants.COLUMN_IDX_TO_LETTER

    def play_turn(self, state):

        # get move input
        next_state = None
        if self.winning_token == Player.COLOR_WIN:
            player_type = "Color Player"
        else:
            player_type = "Dots Player"
        while not next_state:
            move = input("Human {} enter your move (0 orientation column row)\n".format(player_type)).split()
            next_state = self.next_turn(move, state)
        return next_state

    def next_turn(self, move, state):
        """
        Moves the game state to the next turn. Handles switching active players, getting inputs and checking for victory
        :return: None
        """

        if self.validate_input(move, state):

            if not state.recycling_mode:
                # play card
                orientation = int(move[1])
                col = self.columns[move[2]] - 1
                row = int(move[3]) - 1
                coord = (row, col)
                card = Card(id=state.turn_number, orientation=orientation, coords=coord)

                next_state = self.play_card(card, state)
                if next_state:
                    return next_state
                else:
                    print('ILLEGAL MOVE')
                    return None
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
                next_state = self.recycle_card((old_row1, old_col1), (old_row2, old_col2), new_card, state)
                if next_state:
                    return next_state
                    # move to Double card
                    # print('Played a card at coordinate {}:{}'.format(self.column_idx_to_letter[col], row + 1))
                else:
                    print('ILLEGAL MOVE')
                    return None

            # set next player's turn
            # MOVE
            # state.active_player = not state.active_player

    def validate_input(self, move, state):
            """
            Makes sure the input is valid
            :return: False if error in input, True otherwise
            """
            if not state.recycling_mode:
                # check arg length
                if len(move) != 4:
                    print('ERROR: incorrect number of arguments, expected 4 instead of {}'.format(len(move)))
                    return False

                # check first arg is 0
                if move[0] != '0':
                    print('ERROR: incorrect first argument, expected 0 instead of {}'.format(move[0]))
                    return False

                # check for valid orientation
                if not self.is_valid_orientation(move[1]):
                    return False

                # check for valid column
                if not self.is_valid_col(move[2]):
                    return False

                # check for valid row
                if not self.is_valid_row(move[3]):
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

    @staticmethod
    def is_valid_row(row):
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

    @staticmethod
    def is_valid_orientation(orientation):
        """
        Checks for valid orientation
        :return: False if invalid, True otherwise
        """

        if not orientation.isdigit() or int(orientation) > 8:
            print('ERROR: incorrect orientation, expected number between 1 and 8 instead of {}'.format(orientation))
            return False
        return True

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
            print('Exceeds limits of the board: {}:{}'.format(card.coords2[0] + 1,
                                                              self.column_idx_to_letter[card.coords2[1]]))
            return False

        # Ensure the cells in which the card will be placed are empty
        if board[card.coords1].card or board[card.coords2].card:
            print('There are already cards at cells: {}:{} or {}:{}'
                  .format(row + 1, self.column_idx_to_letter[col], other_row + 1, self.column_idx_to_letter[other_col]))
            return False

        # Ensure that cells underneath card is not empty
        if row > 0:
            if card.horizontal:
                empty_below = not board[row - 1][col].card or not board[row - 1][col + 1].card
                if empty_below:
                    print('Cards cannot float above empty location: {}:{} or {}:{} is empty'
                          .format(row, self.column_idx_to_letter[col], row, self.column_idx_to_letter[col + 1]))
                return not empty_below
            else:
                empty_below = not board[row - 1][col].card
                if empty_below:
                    print('Cards cannot float above empty location: {}:{} is empty'
                          .format(row, self.column_idx_to_letter[col]))
                return not empty_below

        # If none of the exit conditions were met, this move is valid
        return True

    def play_card(self, card, state, old_coord=None):
        """
        Plays a card at a given location on the board
        :param card: the card while being placed
        :param state: The state of the game
        :param old_coord: the old coordinates of the card to remove from the board
        :return: the next state if a valid card was played, None otherwise
        """

        if self.valid_move(card, state.board):
                # Place card in the board
                # set board cell values
                BoardHelper.fill_cells(card, state)
                
                if old_coord:
                    self.display.remove_piece(*old_coord)
                self.display.add_piece(state.board[card.coords1])

                # Check if this move triggers a victory condition
                if BoardHelper.victory_move(card.coords1, state) or \
                        BoardHelper.victory_move(card.coords2, state):
                    print("Victory condition was met!")
                    state.game_over = True
                # after playing card set last moved card id
                state.last_moved_card = card
                return state
        else:
            return None

    def recycle_card(self, coord1, coord2, new_card, state):
        """
        Moves a card from one location to another on the board
        :param coord1: The 1st coordinate at which the player attempts to take a card
        :param coord2: The 2nd coordinate at which the player attempts to take a card
        :param new_card: The coordinate at which the player attempts to place the card
        :param state: The current state of the board that will be modified
        :return: True if a valid card was played, false otherwise
        """

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
            return None

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
            return None

        # Ensure that the card is in either a new coord or orientation
        # check coord. of first half
        if old_card.orientation == new_card.orientation and old_card.coords1 == new_card.coords1:
            print('Cannot recycle card, either coordinate or orientation of card must change')
            return None

        # check if current card is the same as last card played
        if state.last_moved_card.id == old_card.id:
            print('Last card was moved from: {}:{}, you cannot move this card again this turn'
                  .format(coord1[0], self.column_idx_to_letter[coord1[1]]))
            return None

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
        next_state = self.play_card(new_card, state, old_card.coords1)
        if next_state:
            # set last moved card
            next_state.last_moved_card = new_card
            return next_state
        else:
            # error was found recycling card
            # Place the old card back in place
            BoardHelper.fill_cells(old_card, state)
            return None
