import tkinter as tk
import math
import sys
import os

from threading import Thread

from DoubleCard import Orientation, Cell, Dir

def closeProgram():
    os._exit(0)

class BoardDisplay(Thread):

    def __init__(self, rows, columns, pixelPerGridSquare):
        Thread.__init__(self)
        self.num_rows = rows + 2  # extra rows for grid labeling
        self.num_cols = columns + 2  # extra cols for grid labeling
        self.pixelPerGridSquare = pixelPerGridSquare
        self.width = self.pixelPerGridSquare * self.num_cols
        self.height = self.pixelPerGridSquare * self.num_rows
        self.pieces = {}
        self.display = None
        self.canvas = None

    def add_piece(self, row, col, orientation):
        cell1X = (col + 1) * self.pixelPerGridSquare
        cell2X = ((col + 1) + orientation.offset[1]) * self.pixelPerGridSquare

        cell1Y = (self.pixelPerGridSquare * (self.num_rows - 1)) - ((row + 1) * self.pixelPerGridSquare)
        cell2Y = (self.pixelPerGridSquare * (self.num_rows - 1)) - (((row + 1) + orientation.offset[0]) * self.pixelPerGridSquare)

        cell1BackgroundColor = "red" if (orientation.cell1 == Cell.RED_EMPTY or orientation.cell1 == Cell.RED_FILLED) else "white"
        cell2BackgroundColor = "red" if (orientation.cell2 == Cell.RED_EMPTY or orientation.cell2 == Cell.RED_FILLED) else "white"

        cell1CircleFilled = (orientation.cell1 == Cell.RED_FILLED or orientation.cell1 == Cell.WHITE_FILLED)
        cell2CircleFilled = (orientation.cell2 == Cell.RED_FILLED or orientation.cell2 == Cell.WHITE_FILLED)

        self.pieces[(row, col)] = (cell1X, cell1Y, cell1BackgroundColor, cell1CircleFilled, cell2X, cell2Y, cell2BackgroundColor, cell2CircleFilled)
    
    def removePiece(self, row, col):
        del self.pieces[(row, col)]

    def run(self):
        self.display = tk.Tk()
        self.display.title("Deep Garbagio")
        self.display.resizable(False, False)
        self.display.protocol("WM_DELETE_WINDOW", closeProgram)
        self.canvas = tk.Canvas(self.display, width=self.width, height=self.height)
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

            # side borders
            self.canvas.create_rectangle(0, 0,
                                         self.pixelPerGridSquare - 1, (self.pixelPerGridSquare * self.num_rows) - 1,
                                         fill="black", width=2)
            self.canvas.create_rectangle(self.pixelPerGridSquare * (self.num_cols - 1), 0,
                                         self.pixelPerGridSquare * self.num_cols, (self.pixelPerGridSquare * self.num_rows) - 1,
                                         fill="black", width=2)

            # top border
            self.canvas.create_polygon(0, 0,
                                       self.pixelPerGridSquare * self.num_cols, 0,
                                       self.pixelPerGridSquare * (self.num_cols - 1), self.pixelPerGridSquare - 1,
                                       self.pixelPerGridSquare - 1, self.pixelPerGridSquare,
                                       fill="#2F2F2F", width=2)
            #bottom border
            self.canvas.create_polygon(0, self.pixelPerGridSquare * self.num_rows,
                                       self.pixelPerGridSquare - 1, self.pixelPerGridSquare*(self.num_rows - 1),
                                       self.pixelPerGridSquare*(self.num_cols - 1), self.pixelPerGridSquare*(self.num_rows - 1),
                                       self.pixelPerGridSquare * self.num_cols, self.pixelPerGridSquare*self.num_rows,
                                       fill="#2F2F2F", width=2)

            # drawing grid labeling
            horizontal_label = tk.Label(self.display, text='A  B  C  D  E  F  G  H', fg="white",
                                        bg="#2F2F2F", font="Courier 22")
            vertical_label = tk.Label(self.display, text='12\n\n11\n\n10\n\n9\n\n8\n\n7\n\n6\n\n5\n\n4\n\n3\n\n2\n\n1', fg="white",
                                        bg="black", font="Courier 17")

            self.canvas.create_window((self.pixelPerGridSquare*self.num_cols) / 2, self.pixelPerGridSquare*(self.num_rows - 0.5), window=horizontal_label)
            self.canvas.create_window(self.pixelPerGridSquare / 2, (self.pixelPerGridSquare*self.num_rows) / 2, window=vertical_label)

            # draw pieces
            for piece in self.pieces.values():
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
