import numpy as np


class DoubleCard:

    def __init__(self):

        self.num_rows = 12
        self.num_cols = 8
        self.board = np.zeros((self.num_rows, self.num_cols))
        self.active_player = None

    def next_turn(self):
        """
        Moves the game state to the next turn. Handles switching active players, getting inputs and checking for victory
        :return: None
        """
        pass

    def play_card(self, coord, orientation):
        """
        Plays a card at a given location on the board
        :param coord: The coordinate at which the player attempts to place the card
        :param orientation: the orientation of the card while being placed
        :return: True if a valid card was played, false otherwise
        """
        pass

    def valid_move(self, coord, orientation):
        """
        Checks if a card can legally be played at a given location on the board
        :param coord: The coordinate at which the player attempts to place the card
        :param orientation: the orientation of the card while being placed
        :return: True if the play is valid, false otherwise
        """

    def victory_move(self, coord, orientation):
        """
        Checks if the placement of the new card triggered a victory
        :param coord: The coordinate at which the player places the card
        :param orientation: the orientation of the card while being placed
        :return: True if the play triggers a victory, false otherwise
        """