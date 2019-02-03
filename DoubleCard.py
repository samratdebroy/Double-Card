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

    def recycle_card(self, old_coord, new_coord, orientation):
        """
        Moves a card from one location to another on the board
        :param old_coord: The coordinate at which the player attempts to take a card
        :param new_coord: The coordinate at which the player attempts to place the card
        :param orientation: the orientation of the card while being placed
        :return: True if a valid card was played, false otherwise
        """
        pass

    def valid_move(self, coord, orientation, board):
        """
        Checks if a card can legally be played at a given location on the board
        :param coord: The coordinate at which the player attempts to place the card
        :param orientation: the orientation of the card while being placed
        :param board: The board on which to check if the move is valid
        :return: True if the play is valid, false otherwise
        """

    def victory_move(self, coord, orientation, board):
        """
        Checks if the placement of the new card triggered a victory
        :param coord: The coordinate at which the player places the card
        :param orientation: the orientation of the card while being placed
        :param board: The board on which to check if victory has been achieved
        :return: True if the play triggers a victory, false otherwise
        """

    def visualize_board(self, board):
        """
        Display the current state of the given board
        :param board: The board to be visualized
        :return: None
        """
        pass
