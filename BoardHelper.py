from Cell import Cell


def fill_cells(card, state):
    board = state.board
    orientation = card.orientation
    # set the cell values for recently played card
    if orientation == 1 or orientation == 4:
        board[card.coords1].color = Cell.RED
        board[card.coords1].fill = Cell.FILLED

        board[card.coords2].color = Cell.WHITE
        board[card.coords2].fill = Cell.OPEN

    elif orientation == 2 or orientation == 3:
        board[card.coords1].color = Cell.WHITE
        board[card.coords1].fill = Cell.OPEN

        board[card.coords2].color = Cell.RED
        board[card.coords2].fill = Cell.FILLED

    elif orientation == 6 or orientation == 7:
        board[card.coords1].color = Cell.WHITE
        board[card.coords1].fill = Cell.FILLED

        board[card.coords2].color = Cell.RED
        board[card.coords2].fill = Cell.OPEN
    else:
        board[card.coords1].color = Cell.RED
        board[card.coords1].fill = Cell.OPEN

        board[card.coords2].color = Cell.WHITE
        board[card.coords2].fill = Cell.FILLED

    board[card.coords1].card = card
    board[card.coords2].card = card
    board[card.coords1].other = board[card.coords2]
    board[card.coords2].other = board[card.coords1]

    #  Update the state of the highest empty cell in the newly occupied columns
    if card.horizontal:
        state.top_empty_cell[card.coords1[1]] = card.coords1[0] + 1
        state.top_empty_cell[card.coords2[1]] = card.coords2[0] + 1
    else:
        state.top_empty_cell[card.coords1[1]] = max(card.coords1[0] + 1, card.coords2[0] + 1)


def remove_cells(coord1, coord2, state):
    # set the cell values for recently removed card
    state.board[coord1].clear()
    state.board[coord2].clear()

    #  Update the state of the highest empty cell in the newly unoccupied columns
    state.top_empty_cell[coord1[1]] -= 1
    state.top_empty_cell[coord2[1]] -= 1
