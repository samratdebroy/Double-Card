import copy
from Player import Player
from GameConstants import GameConstants
from Card import Card
from Cell import Cell
import BoardHelper


class AIPlayer(Player):

    def __init__(self, winning_token, display):
        Player.__init__(self, winning_token, display)

    def play_turn(self, state):
        maximizing_player = (self.winning_token == Player.COLOR_WIN)

        # Grab the next desired state from the minimax algorithm
        if GameConstants.DEMO_MODE:
            next_state, _ = mini_max(state, GameConstants.MINI_MAX_DEPTH, maximizing_player, demo_heuristic)
        else:
            # TODO: Implement the comp heuristic and remove the line below
            competition_heuristic = None
            next_state, _ = mini_max(state, GameConstants.MINI_MAX_DEPTH, maximizing_player, competition_heuristic)

        # Update the board display
        if next_state.recycling_mode:
            removed_card = state.cards[next_state.last_moved_card.id]
            coord1 = removed_card.coords1
            self.display.remove_piece(coord1[0], coord1[1])
        card = next_state.last_moved_card
        self.display.add_piece(next_state.board[card.coords1])

        # Update the Board State
        return next_state


def generate_next_board_states(state):
    """
    Generates a list of board states from all the possible next legal moves
    :param state: Current board state from which the next legal moves will be evaluated
    :return: list of board states from all the possible next legal moves
    """

    # If the max number of turns has been reached, then the game is over
    if state.turn_number == GameConstants.MAX_TURN_NUMBER or state.game_over:
        state.game_over = True
        return []

    state_list = list()
    # Generate a new state with updated meta data for the next turn
    new_state = copy.deepcopy(state)
    new_state.turn_number += 1
    new_state.recycling_mode = new_state.turn_number >= GameConstants.MAX_CARDS_IN_GAME
    new_state.active_player = not state.active_player


    if not state.recycling_mode:
        for next_state in generate_next_placed_board_states(new_state):
            yield next_state
    else:
        # For each card you can remove, make a new state and call generate_next_placed_board_states on it
        # Append all the possible next states into a super list of board states and return
        states_with_removed_cards = generate_next_removed_board_states(state)
        for state, old_card in states_with_removed_cards:
            state_list.extend(generate_next_placed_board_states(state, old_card))

    # For each state generated, check if it triggered a victory condition and set its game_over values appropriately
    for state in state_list:
        BoardHelper.victory_move(state.last_moved_card.coords1, state)
        BoardHelper.victory_move(state.last_moved_card.coords2, state)

    return state_list


def generate_next_placed_board_states(state, old_card=None):
    """
    Generates a list of board states where cards have been legally placed
    :param state: The state to which cards will be placed
    :param old_card: If we're in recycling mode we track the card that was just removed
    :return: A list of all states that can be generated by legally placing a card in the given input state
    """

    if old_card:
        new_id = old_card.id
    else:
        new_id = state.turn_number

    # Pass through every empty cell at the top of a column and place cards there
    for col, row in enumerate(state.top_empty_cell):

        # This column is filled with cards so ignore
        if row >= GameConstants.NUM_ROWS:
            continue

        if row < GameConstants.NUM_ROWS - 1:
            #  We can place a card vertically in this column
            for next_State in generate_board_states_placement(state, (row, col), new_id, old_card,
                                                              GameConstants.VERTICAL_ORIENTATIONS):
                yield next_State

        if row < GameConstants.NUM_ROWS and col < GameConstants.NUM_COLS - 1:
            if row == state.top_empty_cell[col + 1]:
                #  We can place a card Horizontally in this column
                for next_State in generate_board_states_placement(state, (row, col), new_id, old_card,
                                                                  GameConstants.HORIZONTAL_ORIENTATIONS):
                    yield next_State


def generate_board_states_placement(state, coord, id, old_card, orientations):
    #  Possible states resulting in the placement of a card
    original_last_moved_card = state.last_moved_card
    if old_card:
        original_old_card = Card(old_card.id, old_card.orientation, old_card.coords1)
    for orientation in orientations:
        # new_state = copy.deepcopy(state)
        new_card = Card(id, orientation, coord)
        # Make sure the card is in a new position orientation
        if old_card and old_card.orientation == new_card.orientation and old_card.coords1 == new_card.coords1:
            continue
        BoardHelper.fill_cells(new_card, state)
        state.last_moved_card = new_card
        yield state

        #  Revert state back to original state
        BoardHelper.remove_cells(state.last_moved_card.coords1, state.last_moved_card.coords2, state)
        if old_card:
            BoardHelper.fill_cells(original_old_card, state)
        state.last_moved_card = original_last_moved_card



def generate_next_removed_board_states(state):

    state_list = list()
    last_horizontal = False
    # Pass through every empty cell at the top of a column and remove cards below
    for col, row in enumerate(state.top_empty_cell):

        # If the last card removed was a horizontal card, then this will be the second cell of the same card, ignore it
        if last_horizontal:
            last_horizontal = False
            continue

        if row > 0:
            card_below = state.board[row - 1, col].card
            if card_below.horizontal:
                if col < GameConstants.NUM_COLS and row == state.top_empty_cell[col + 1] \
                        and card_below is state.board[row - 1, col + 1].card:
                    # This is a legal horizontal card that can be removed
                    last_horizontal = True
                else:
                    # This is a horizontal card that cannot be removed
                    continue

            #  This is a legal vertical or Horizontal card that can be removed
            new_state = copy.deepcopy(state)
            BoardHelper.remove_cells(card_below.coords1, card_below.coords2, new_state)
            state_list.append((new_state, card_below))

    return state_list


def mini_max(state, depth, maximizing_player, heuristic):
    """
    Given the current state of the game, finds next best move using minimax algorithm
    :param state: current board state
    :param depth: maximum depth of minimax tree
    :param maximizing_player: True if the current player is trying to maximize the score
    :param heuristic: The heuristic function called on the board state
    :return: next best move Card object and the value of the winning heuristic
    """
    # return if depth is reached or maximum value is encountered
    if depth <= 0 or state.game_over:
        return state, heuristic(state)

    # recursively call minimax going to node with best value based on level
    if maximizing_player:
        value = float('-inf')
        best_next_state = None
        for next_state in generate_next_board_states(state):
            new_state, new_value = mini_max(next_state, depth - 1, False, heuristic)
            if new_value > value:
                value = new_value
                if depth == GameConstants.MINI_MAX_DEPTH:
                    best_next_state = new_state  # Only want the child of roots to be returned
                else:
                    best_next_state = state
        return best_next_state, value
    else:  # Minimizing Player
        value = float('inf')
        best_next_state = None
        for next_state in generate_next_board_states(state):
            new_state, new_value = mini_max(next_state, depth - 1, True, heuristic)
            if new_value < value:
                value = new_value
                if depth == GameConstants.MINI_MAX_DEPTH:
                    best_next_state = new_state  # Only want the child of roots to be returned
                else:
                    best_next_state = state
        return best_next_state, value


def demo_heuristic(state):
    """
    calculates a heuristic value given the board state
    :param state: BoardState object
    """

    # for professor's heuristic
    # loop through cards list and sum according to specs
    board_sum = 0
    coord = lambda c: c.coordinate[0]*GameConstants.NUM_COLS + c.coordinate[1]
    for card in state.cards.values():
        card_cells = [state.board[card.coords1], state.board[card.coords2]]
        for cell in card_cells:
            if cell.color == Cell.WHITE and cell.fill == Cell.OPEN:
                board_sum += coord(cell)

            elif cell.color == Cell.WHITE and cell.fill == Cell.FILLED:
                board_sum += 3*(coord(cell))

            elif cell.color == Cell.RED and cell.fill == Cell.FILLED:
                board_sum -= 2*(coord(cell))

            elif cell.color == Cell.RED and cell.fill == Cell.OPEN:
                board_sum -= 1.5*(coord(cell))
    return board_sum
