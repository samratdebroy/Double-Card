import tkinter as tk
import math
import os

from threading import Thread
from Cell import Cell


def close_program():
    os._exit(0)


class BoardDisplay(Thread):

    def __init__(self, rows, columns, pixelPerGridSquare, states=None):
        Thread.__init__(self)
        self.num_rows = rows + 2  # extra rows for grid labeling
        self.num_cols = columns + 2  # extra cols for grid labeling
        self.pixelPerGridSquare = pixelPerGridSquare
        self.width = self.pixelPerGridSquare * self.num_cols
        self.height = self.pixelPerGridSquare * self.num_rows
        self.pieces = []
        self.num_states = None
        self.state_id = 0
        # Generate a board display for each given state
        if states:
            self.num_states = len(states)
            for state_id, state in enumerate(states):
                self.pieces.append({})
                self.state_id = state_id
                for cell in state.board.flatten():
                    if cell.card:
                        self.add_piece(cell)
        else:
            self.pieces.append({})

        self.display = None
        self.canvas = None
        self.vertical_label = None
        self.horizontal_label = None
        self.button = None

    def next_state_callback(self):
        if self.num_states:
            self.state_id = (self.state_id + 1) % (self.num_states - 1)
            self.button["text"] = "state {}".format(self.state_id)

    def add_piece(self, cell):
        card = cell.card
        row, col = card.coords1
        row2, col2 = card.coords2

        cell1X = (col + 1) * self.pixelPerGridSquare
        cell2X = (col2 + 1) * self.pixelPerGridSquare

        cell1Y = (self.pixelPerGridSquare * (self.num_rows - 1)) - ((row + 1) * self.pixelPerGridSquare)
        cell2Y = (self.pixelPerGridSquare * (self.num_rows - 1)) - ((row2 + 1) * self.pixelPerGridSquare)

        cell1BackgroundColor = "red" if (cell.color == Cell.RED) else "white"
        cell2BackgroundColor = "red" if (cell.other.color == Cell.RED) else "white"

        cell1CircleFilled = cell.fill == Cell.FILLED
        cell2CircleFilled = cell.other.fill == Cell.FILLED

        self.pieces[self.state_id][(row, col)] = (cell1X, cell1Y, cell1BackgroundColor, cell1CircleFilled, cell2X, cell2Y,
                                   cell2BackgroundColor, cell2CircleFilled)
    
    def remove_piece(self, row, col, state_idx=0):
        del self.pieces[state_idx][(row, col)]

    def run(self):
        self.display = tk.Tk()
        self.display.title("Deep Garbagio")
        self.display.resizable(False, False)
        self.display.protocol("WM_DELETE_WINDOW", close_program)
        self.canvas = tk.Canvas(self.display, width=self.width, height=self.height)
        self.canvas.pack()
        self.canvas.after(16, self._redraw)
        self.horizontal_label = tk.Label(self.display, text='A  B  C  D  E  F  G  H', fg="white",
                                        bg="#2F2F2F", font="Courier 22")
        self.vertical_label = tk.Label(self.display, text='12\n\n11\n\n10\n\n9\n\n8\n\n7\n\n6\n\n5\n\n4\n\n3\n\n2\n\n1',
                                       fg="white", bg="black", font="Courier 17")
        self.button = tk.Button(self.display, text="next", command=self.next_state_callback)
        self.button.pack()
        tk.mainloop()

    def _redraw(self):
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
                                         self.pixelPerGridSquare * self.num_cols,
                                         (self.pixelPerGridSquare * self.num_rows) - 1, fill="black", width=2)

            # top border
            self.canvas.create_polygon(0, 0,
                                       self.pixelPerGridSquare * self.num_cols, 0,
                                       self.pixelPerGridSquare * (self.num_cols - 1), self.pixelPerGridSquare - 1,
                                       self.pixelPerGridSquare - 1, self.pixelPerGridSquare,
                                       fill="#2F2F2F", width=2)
            # bottom border
            self.canvas.create_polygon(0, self.pixelPerGridSquare * self.num_rows,
                                       self.pixelPerGridSquare - 1, self.pixelPerGridSquare*(self.num_rows - 1),
                                       self.pixelPerGridSquare*(self.num_cols - 1),
                                       self.pixelPerGridSquare*(self.num_rows - 1),
                                       self.pixelPerGridSquare * self.num_cols, self.pixelPerGridSquare*self.num_rows,
                                       fill="#2F2F2F", width=2)

            # drawing grid labeling
            self.canvas.create_window((self.pixelPerGridSquare*self.num_cols) / 2,
                                      self.pixelPerGridSquare*(self.num_rows - 0.5), window=self.horizontal_label)
            self.canvas.create_window(self.pixelPerGridSquare / 2, (self.pixelPerGridSquare*self.num_rows) / 2,
                                      window=self.vertical_label)

            # draw pieces
            for piece in self.pieces[self.state_id].copy().values():
                # draw squares
                self.canvas.create_rectangle(piece[0], piece[1],
                                             piece[0] + self.pixelPerGridSquare, piece[1] + self.pixelPerGridSquare,
                                             fill=piece[2], width=0)
                self.canvas.create_rectangle(piece[4], piece[5],
                                             piece[4] + self.pixelPerGridSquare, piece[5] + self.pixelPerGridSquare,
                                             fill=piece[6], width=0)

                # draw circles
                radius = math.floor(self.pixelPerGridSquare * 0.1)
                cell1CenterX = math.floor(piece[0] + (self.pixelPerGridSquare / 2.0))
                cell1CenterY = math.floor(piece[1] + (self.pixelPerGridSquare / 2.0))
                self.canvas.create_oval(cell1CenterX - radius, cell1CenterY - radius, cell1CenterX + radius,
                                        cell1CenterY + radius, fill="black" if piece[3] else "")

                cell2CenterX = math.floor(piece[4] + (self.pixelPerGridSquare / 2.0))
                cell2CenterY = math.floor(piece[5] + (self.pixelPerGridSquare / 2.0))
                self.canvas.create_oval(cell2CenterX - radius, cell2CenterY - radius, cell2CenterX + radius,
                                        cell2CenterY + radius, fill="black" if piece[7] else "")

            # Draw card borders
            for piece in self.pieces[self.state_id].copy().values():
                border_x = min(piece[0], piece[4])
                border_y = min(piece[1], piece[5])
                border_x_max = max(piece[0] + self.pixelPerGridSquare, piece[4] + self.pixelPerGridSquare)
                border_y_max = max(piece[1] + self.pixelPerGridSquare, piece[5] + self.pixelPerGridSquare)
                self.canvas.create_rectangle(border_x, border_y, border_x_max, border_y_max, fill='', width=5)

            self.canvas.after(16, self._redraw)
