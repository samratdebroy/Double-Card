from Player import Player


class HumanPlayer(Player):

    def __init__(self, winning_token):
        Player.__init__(self, winning_token)

    def play_turn(self, state, display):
        pass
