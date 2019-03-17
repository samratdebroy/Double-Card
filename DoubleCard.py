import time
from GameConstants import GameConstants
from Cell import Cell
from BoardState import BoardState
from BoardDisplay import BoardDisplay
from HumanPlayer import HumanPlayer
from AIPlayer import AIPlayer
from Player import Player
import cProfile, pstats, io
import heuristics

class DoubleCard:

    def __init__(self):
        self.state = BoardState()
        self.display = BoardDisplay(GameConstants.NUM_ROWS, GameConstants.NUM_COLS, 50)
        self.verbose_output = True  # Set to true if you want to see board state in the console after each move
        self.animate = False  # Set to true if you want to see board build itself when running tests
        self.alpha_beta = False  # set the AI algorithm to use alpha beta pruning
        self.players = list()  # list of players
        self.test_player = None
        self.profile = False

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
            self.test_player = HumanPlayer(0, self.display)

        # self.alpha_beta = (input("Are you playing with alpha_beta (y) or not (n) \n") == 'y')

        # GameConstants.TRACE_MODE = (input("Do you have the program to generate a trace file? (y) or not (n) \n") == 'y')

        is_human = int(input("Is Player 1 a Human (0) or an AI (1)\n")) == 0
        if is_human:
            self.players.append(HumanPlayer(None, self.display))
        else:
            self.players.append(AIPlayer(None, self.display, heuristic=heuristics.open_competition_heuristic))

        is_human = int(input("Is Player 2 a Human (0) or an AI (1)\n")) == 0
        if is_human:
            self.players.append(HumanPlayer(None, self.display))
        else:
            self.players.append(AIPlayer(None, self.display, heuristic=heuristics.open_competition_heuristic))

        self.players[0].winning_token = int(input("Is player 1 playing for colors(0) or dots(1)\n"))
        self.players[1].winning_token = int(not self.players[0].winning_token)

        # game loop
        while not self.state.game_over:
            if input_file:
                try:
                    # Test mode
                    move = input_file.readline().split()
                except Exception as err:
                    print('Error {}'.format(err))
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
                    next_state = self.test_player.next_turn(move, self.state)
                    if next_state:
                        self.state = next_state
                        self.print_move()
                        self.increment_turn_number()

            else:
                if self.animate:
                    time.sleep(0.1)
                if self.profile:
                    pr = cProfile.Profile()
                    pr.enable()

                # Extract the new state following the played move
                temp_state = self.players[self.state.active_player].play_turn(self.state)

                if isinstance(self.players[self.state.active_player], AIPlayer):
                    # If an AI just played, extract their last move and play it normally like a human
                    new_move = DoubleCard.extract_last_move(self.state, temp_state)
                    print('AI Play just played ' + str(new_move))

                    # Simulate a move being played with a Human Player
                    dummy_player = HumanPlayer(self.players[self.state.active_player].winning_token, self.display)
                    self.state = dummy_player.next_turn(new_move, self.state)
                else:
                    # If it is a human player, play turn will return the proper next state
                    self.state = temp_state

                if self.profile:
                    pr.disable()
                    s = io.StringIO()
                    # sortby = pstats.SortKey.CUMULATIVE
                    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
                    ps.print_stats()
                    print(s.getvalue())

                self.print_move()
                self.increment_turn_number()

                # Flip active player if current player was not an AI
                self.state.active_player = not self.state.active_player

    @staticmethod
    def extract_last_move(last_state, new_state):

        new_moved_card = new_state.last_moved_card
        # new coordinate should be lower-left coordinate of new card placement
        if new_moved_card.coords1[0] <= new_moved_card.coords2[0]:
            new_coord = new_moved_card.coords1
        else:
            new_coord = new_moved_card.coords2

        col = GameConstants.COLUMN_IDX_TO_LETTER
        if last_state.recycling_mode:
            removed_card = last_state.cards[new_moved_card.id]
            coord1 = removed_card.coords1
            coord2 = removed_card.coords2
            return '{} {} {} {} {} {} {}'.format(col[coord1[1]], coord1[0] + 1, col[coord2[1]], coord2[0] + 1,
                                                 new_moved_card.orientation, col[new_coord[1]],
                                                 new_coord[0] + 1).split()
        else:
            return '{} {} {} {}'.format(0, new_moved_card.orientation, col[new_coord[1]],
                                        new_coord[0] + 1).split()

    def increment_turn_number(self):
        self.state.turn_number += 1

        if self.state.turn_number == GameConstants.MAX_TURN_NUMBER:
            self.state.game_over = True
            print('The max turn number has been reached, the game ends in a draw')
        self.set_recycle_mode()

    def print_move(self):
        if self.players[self.state.active_player].winning_token == Player.COLOR_WIN:
            current_player = "Colors player"
        else:
            current_player = "Dots player"

        last_card = self.state.last_moved_card

        print('Turn {}: Player {} placed a card at coordinates {}:{} {}:{}'
              .format(self.state.turn_number, current_player,
                      GameConstants.COLUMN_IDX_TO_LETTER[last_card.coords1[1]],
                      last_card.coords1[0] + 1,
                      GameConstants.COLUMN_IDX_TO_LETTER[last_card.coords2[1]],
                      last_card.coords2[0] + 1))

        if self.state.game_over:
            if self.state.winner == Player.COLOR_WIN:
                print("Colors Player has won the game!!!")
            elif self.state.winner == Player.DOT_WIN:
                print("Dots Player has won the game!!!")

    def set_recycle_mode(self):
        if self.state.turn_number >= GameConstants.MAX_CARDS_IN_GAME:
            self.state.recycling_mode = True

if __name__ == "__main__":
    DoubleCard().play()
