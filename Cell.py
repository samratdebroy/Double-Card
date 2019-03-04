class Cell:
    EMPTY, RED, WHITE, FILLED, OPEN = range(5)

    def __init__(self, coord):
        self.coordinate = coord # Coordinate of the cell in the board
        self.color = None
        self.fill = None
        self.card = None  # Card object referenced in this cell
        self.other = None # Cell containing the other half of the card

    def clear(self):
        self.color = None
        self.fill = None
        self.card = None  # Card object referenced in this cell
        self.other = None # Cell containing the other half of the card

    @staticmethod
    def get_color(cell):
        return cell.color

    @staticmethod
    def get_fill(cell):
        return cell.fill