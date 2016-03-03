#!/usr/bin/env python

"""
This is a solution to the Chess Challenge
"""

import time


def col_row_to_pos(col, row, m):
    """
    Given col, row and m (number of columns) returns the corresponding
    position on the chess board
    """
    return row * m + col


def pos_to_col_row(pos, m):
    """
    Given position and m (number of columns) returns the corresponding
    col, row on the chess board
    """
    row = pos / m
    col = pos % m
    return col, row


class Piece(object):
    """
    Base class for Chess objects
    """

    def get_targets(self, m, n, row, col):
        """
        Given the number of columns and rows (m, n) and the position (row, col)
        returns the list of positions which can be attacked by the item
        """
        raise RuntimeError('Must be implemented!')


class Knight(Piece):
    """
    Class definition for Knight objects
    """
    SYMBOL = 'n'

    def get_targets(self, m, n, row, col):
        """
        Given the number of columns and rows (m, n) and the position (row, col)
        returns the list of positions which can be attacked by the item
        """
        positions = []
        if row > 0:
            if col > 1:
                positions.append((row - 1, col - 2))
            if col + 2 < m:
                positions.append((row - 1, col + 2))
        if row + 1 < n:
            if col > 1:
                positions.append((row + 1, col - 2))
            if col + 2 < m:
                positions.append((row + 1, col + 2))

        if row > 1:
            if col > 0:
                positions.append((row - 2, col - 1))
            if col < m:
                positions.append((row - 2, col + 1))
        if row + 2 < m:
            if col > 0:
                positions.append((row + 2, col - 1))
            if col < m:
                positions.append((row + 2, col + 1))
        return set(positions)


class King(Piece):
    """
    Class definition for King objects
    """
    SYMBOL = 'k'

    def get_targets(self, m, n, row, col):
        """
        Given the number of columns and rows (m, n) and the position (row, col)
        returns the list of positions which can be attacked by the item
        """
        positions = []
        if row > 0:
            positions.append((row - 1, col))
            if col > 0:
                positions.append((row - 1, col - 1))
            if col + 1 < m:
                positions.append((row - 1, col + 1))
        if row + 1 < m:
            positions.append((row + 1, col))
            if col > 0:
                positions.append((row + 1, col - 1))
            if col + 1 < m:
                positions.append((row + 1, col + 1))
        if col > 0:
            positions.append((row, col - 1))
        if col + 1 < n:
            positions.append((row, col + 1))
        return set(positions)


class Rook(Piece):
    """
    Class definition for Rook objects
    """
    SYMBOL = 'r'

    def get_targets(self, m, n, row, col):
        """
        Given the number of columns and rows (m, n) and the position (row, col)
        returns the list of positions which can be attacked by the item
        """
        positions = {(row, x) for x in range(m)}
        positions |= {(x, col) for x in range(n)}

        return positions - {(row, col)}


class Queen(Piece):
    """
    Class definition for Queen objects
    """
    SYMBOL = 'q'

    def get_targets(self, m, n, row, col):
        """
        Given the number of columns and rows (m, n) and the position (row, col)
        returns the list of positions which can be attacked by the item
        """
        positions = Rook().get_targets(m, n, row, col)
        positions |= Bishop().get_targets(m, n, row, col)

        return positions - {(row, col)}


class Bishop(Piece):
    """
    Class definition for Bishop objects
    """
    SYMBOL = 'b'

    def get_targets(self, m, n, row, col):
        """
        Given the number of columns and rows (m, n) and the position (row, col)
        returns the list of positions which can be attacked by the item
        """
        positions = set(zip(reversed(range(row)), range(col + 1, m)))
        positions |= set(zip(range(row + 1, n), reversed(range(col))))
        positions |= set(zip(reversed(range(row)), reversed(range(col))))
        positions |= set(zip(range(row + 1, n), range(col + 1, m)))

        return positions


piece_to_class = {
    Knight.SYMBOL: Knight(),
    Rook.SYMBOL: Rook(),
    King.SYMBOL: King(),
    Bishop.SYMBOL: Bishop(),
    Queen.SYMBOL: Queen(),
}


def place_piece(pieces, m, n, row, col, unique_configs, occupied_positions,
                prohibited_positions):
    """
    Recursively tries to place pieces on chess board and returns the unique
    configurations
    :param pieces: Pieces to place on board
    :param m: Number of columns
    :param n: Number of rows
    :param row: row to put the piece on
    :param col: col to put the piece on
    :param unique_configs: list of configurations to be returned
    :param occupied_positions: positions already occupied by pieces
    :param prohibited_positions: positions that can be attacked by pieces
    already placed
    :return: unique configurations of the chess board
    """
    pieces = {key: value for key, value in pieces.items() if value}
    if not pieces:
        unique_configs += [occupied_positions]
        return

    if col_row_to_pos(col, row, m) >= m * n:
        return

    if (row, col) in prohibited_positions:
        next_col, next_row = get_next_col_row(col, row, m)
        return place_piece(pieces.copy(), m, n, next_row, next_col,
                           unique_configs, occupied_positions.copy(),
                           prohibited_positions.copy())

    for p in pieces:
        targets = piece_to_class[p].get_targets(m, n, row, col)
        if occupied_positions & targets:
            continue
        new_occupied_positions = occupied_positions | {(row, col)}
        new_prohibited_positions = prohibited_positions | targets
        new_pieces = pieces.copy()
        new_pieces[p] -= 1
        next_col, next_row = get_next_col_row(col, row, m)
        place_piece(new_pieces, m, n, next_row, next_col, unique_configs,
                    new_occupied_positions,
                    new_prohibited_positions)

    next_col, next_row = get_next_col_row(col, row, m)
    place_piece(pieces.copy(), m, n, next_row, next_col, unique_configs,
                occupied_positions.copy(),
                prohibited_positions.copy())


def get_next_col_row(col, row, m):
    """Given col, row, m (number of columns) returns the next col, row"""
    return pos_to_col_row(col_row_to_pos(col, row, m) + 1, m)


def get_unique_configurations(m, n, pieces):
    """
    Returns the unique chess board configurations for the given parameters
    """
    occupied_positions = set()
    prohibited_positions = set()
    unique_configs = []
    place_piece(pieces, m, n, 0, 0, unique_configs, occupied_positions,
                prohibited_positions)
    return unique_configs


if __name__ == '__main__':
    start = time.time()
    configurations1 = get_unique_configurations(3, 3, {'k': 2, 'r': 1})
    configurations2 = get_unique_configurations(4, 4, {'r': 2, 'n': 4})
    configurations3 = get_unique_configurations(5, 5, {'r': 2, 'n': 4})
    print "Takes {}".format(time.time() - start)
    print configurations1
    print configurations2
