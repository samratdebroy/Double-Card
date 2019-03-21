class GameConstants:
    NUM_ROWS = 12
    NUM_COLS = 8
    MAX_CARDS_IN_GAME = 24  # The total number of cards split among both players; Affects recycling mode timing
    MAX_TURN_NUMBER = 60  # The max turns the game can run for before a draw is concluded
    VERTICAL_ORIENTATIONS = [2, 4, 6, 8]
    HORIZONTAL_ORIENTATIONS = [1, 3, 5, 7]
    MINI_MAX_DEPTH = 2
    ORIG_MINI_MAX_DEPTH = 2     # This is the Mini Max Depth that you should change
    DEMO_MODE = False
    TRACE_MODE = False
    COLUMNS = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8}  # Column label mapping
    COLUMN_IDX_TO_LETTER = 'ABCDEFGH'
