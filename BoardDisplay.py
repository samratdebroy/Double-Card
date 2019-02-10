import tkinter as tk
import math

from threading import Thread

from DoubleCard import Orientation, Cell, Dir

class BoardDisplay(Thread):

    def __init__(self, rows, columns, pixelPerGridSquare):
        Thread.__init__(self)
        self.num_rows = rows
        self.num_cols = columns
        self.pixelPerGridSquare = pixelPerGridSquare
        self.width = self.pixelPerGridSquare * self.num_cols
        self.height = self.pixelPerGridSquare * self.num_rows
        self.pieces = []
        self.canvas = None

    def addPiece(self, row, col, orientation):
        cell1X = col * self.pixelPerGridSquare
        cell2X = (col + orientation.offset[1]) * self.pixelPerGridSquare

        cell1Y = self.height - ((row + 1) * self.pixelPerGridSquare)
        cell2Y = self.height - (((row + 1) + orientation.offset[0]) * self.pixelPerGridSquare)

        cell1BackgroundColor = "red" if (orientation.cell1 == Cell.RED_EMPTY or orientation.cell1 == Cell.RED_FILLED) else "white"
        cell2BackgroundColor = "red" if (orientation.cell2 == Cell.RED_EMPTY or orientation.cell2 == Cell.RED_FILLED) else "white"
        
        cell1CircleFilled = (orientation.cell1 == Cell.RED_FILLED or orientation.cell1 == Cell.WHITE_FILLED)
        cell2CircleFilled = (orientation.cell2 == Cell.RED_FILLED or orientation.cell2 == Cell.WHITE_FILLED)

        self.pieces.append((cell1X, cell1Y, cell1BackgroundColor, cell1CircleFilled, cell2X, cell2Y, cell2BackgroundColor, cell2CircleFilled))

    def run(self):
        display = tk.Tk()
        self.canvas = tk.Canvas(display, width=self.width, height=self.height)
        self.canvas.pack()
        self.canvas.after(16, self.__redraw)
        tk.mainloop()

    def __redraw(self):
        if self.canvas is not None:
            self.canvas.delete(tk.ALL)

            # draw grid
            for row in range(self.num_rows):
                self.canvas.create_line(0, row * self.pixelPerGridSquare, self.width, row * self.pixelPerGridSquare)

            for col in range(self.num_cols):
                self.canvas.create_line(col * self.pixelPerGridSquare, 0, col * self.pixelPerGridSquare, self.height)

            # draw pieces
            for piece in self.pieces:
                # draw squares
                self.canvas.create_rectangle(piece[0], piece[1], piece[0] + self.pixelPerGridSquare, piece[1] + self.pixelPerGridSquare, fill=piece[2], width=2)
                self.canvas.create_rectangle(piece[4], piece[5], piece[4] + self.pixelPerGridSquare, piece[5] + self.pixelPerGridSquare, fill=piece[6], width=2)

                # draw circles
                radius = math.floor(self.pixelPerGridSquare * 0.1)
                cell1CenterX = math.floor(piece[0] + (self.pixelPerGridSquare / 2.0))
                cell1CenterY = math.floor(piece[1] + (self.pixelPerGridSquare / 2.0))
                self.canvas.create_oval(cell1CenterX - radius, cell1CenterY - radius, cell1CenterX + radius, cell1CenterY + radius, fill="black" if piece[3] else "")

                cell2CenterX = math.floor(piece[4] + (self.pixelPerGridSquare / 2.0))
                cell2CenterY = math.floor(piece[5] + (self.pixelPerGridSquare / 2.0))
                self.canvas.create_oval(cell2CenterX - radius, cell2CenterY - radius, cell2CenterX + radius, cell2CenterY + radius, fill="black" if piece[7] else "")


            self.canvas.after(16, self.__redraw)
