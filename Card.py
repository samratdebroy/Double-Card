import numpy as np
from Dir import Dir


class Card:

    def __init__(self, id,  orientation, coords):

        self.id = id
        self.orientation = orientation
        self.horizontal = False
        self.coords1 = coords
        self.coords2 = np.zeros(2)

        if orientation % 2 == 0:
            # Vertical card
            self.horizontal = False
            coord = self.coords1 + Dir.UP
            self.coords2 = tuple(coord.tolist())  # Convert Numpy array to tuple
        else:
            # Horizontal card
            self.horizontal = True
            coord = self.coords1 + Dir.RIGHT
            self.coords2 = tuple(coord.tolist())

