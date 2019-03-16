import numpy as np


class Dir:
    UP = np.array((1, 0))
    DOWN = np.array((-1, 0))
    LEFT = np.array((0, -1))
    RIGHT = np.array((0, 1))
    DIAG_UR = np.array((1,1))
    DIAG_UL = np.array((1,-1))
    DIAG_DR = np.array((-1, 1))
    DIAG_DL = np.array((-1,-1))
