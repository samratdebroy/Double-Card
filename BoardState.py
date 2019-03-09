import numpy as np
from GameConstants import GameConstants
import copy

class BoardState:

    def __init__(self):
        self.turn_number = 0
        self.last_moved_card = None
        self.recycling_mode = False
        self.game_over = False
        self.board = np.empty((GameConstants.NUM_ROWS, GameConstants.NUM_COLS), dtype=object)
        self.top_empty_cell = np.zeros(GameConstants.NUM_COLS, dtype=int)  # List of highest empty cell per column
        self.active_player = False
        self.heuristic_value = None
        self.winner = None  # Set to Player.COLOR_WIN or Player.DOT_WIN
        self.cards = dict()  # list of cards on board

        ''' def __deepcopy__(self, memodict={}):
        new_inst = BoardState()
        new_inst.turn_number = self.turn_number
        new_inst.recycling_mode = self.recycling_mode
        new_inst.game_over = self.game_over
        new_inst.top_empty_cell = self.top_empty_cell.copy()
        new_inst.board = self.board.copy()
        new_inst.active_player = self.active_player
        new_inst.heuristic_value = self.heuristic_value
        new_inst.winner = self.winner
        new_inst.cards = copy.deepcopy(self.cards)
        if self.last_moved_card:
            new_inst.last_moved_card = new_inst.cards[self.last_moved_card.id]
        return new_inst
        '''

