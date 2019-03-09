import numpy as np
from GameConstants import GameConstants


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
