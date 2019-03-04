import numpy as np
from GameConstants import GameConstants


class BoardState:

    def __init__(self):
        self.turn_number = 0
        self.last_moved_card_id = None
        self.recycling_mode = False
        self.game_over = False
        self.board = np.empty((GameConstants.NUM_ROWS, GameConstants.NUM_COLS), dtype=object)
        self.top_cards = list()  # List of row index where highest card per column is located
        self.active_player = False
