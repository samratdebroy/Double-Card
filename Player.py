import abc


class Player(abc.ABC):
    # Winning token
    COLOR_WIN = 0
    DOT_WIN = 1

    def __init__(self, winning_token):
        self.winning_token = winning_token

    # Override in derived class
    @abc.abstractmethod
    def play_turn(self):
        pass
