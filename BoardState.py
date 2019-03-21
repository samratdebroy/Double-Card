import numpy as np
from GameConstants import GameConstants
from Cell import Cell
from Card import Card
import BoardHelper
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
        self.maximizing = False

    def __deepcopy__(self, memodict={}):
        new_inst = BoardState()

        # Initialize the board with empty cells
        for row in range(GameConstants.NUM_ROWS):
            for col in range(GameConstants.NUM_COLS):
                new_inst.board[row, col] = Cell((row, col))

        new_inst.turn_number = int(self.turn_number)
        new_inst.recycling_mode = bool(self.recycling_mode)
        new_inst.game_over = bool(self.game_over)
        new_inst.active_player = copy.copy(self.active_player)
        new_inst.heuristic_value = float(self.heuristic_value) if self.heuristic_value else None
        new_inst.winner = copy.copy(self.winner)
        for card in self.cards.values():
            new_inst.cards[card.id] = Card(card.id, card.orientation, card.coords1)
            BoardHelper.fill_cells(card, new_inst)  # This will also populate self.top_empty_cell
        if self.last_moved_card:
            new_inst.last_moved_card = new_inst.cards[self.last_moved_card.id]
        return new_inst

