#!/usr/bin/env python3

# Copyright (C) 2023  Diogo F. S. Ramos and UFABC Dojo Members
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License.

"""
Plays a game of four-in-a-row.

This program implements the game four-in-a-row, to be played by two
external programs (strategies).

The objective of the game is to place your pieces in a row of four
pieces. The row can be horizontal, vertical, or diagonal.

The board is a matrix of 6 by 7 and each player chooses the column to
place their piece. A piece will rest at the bottom of the board or on
top of another piece.

The following is a representation of an empty board. Each `.' marks
empty space and the top numbers mark the columns.

1 2 3 4 5 6 7
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .

There're two players: @ and O. The first player to move is @, then O.
Each player places their pieces in turns. So after two turns, the
board might look like as

1 2 3 4 5 6 7
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . O . .
. . . . @ . .

where player @ placed their piece at column 5, and then player O too
placed their piece in column 5.

A game ends when four pieces are placed in a row, as in

1 2 3 4 5 6 7
. . . . @ . O
. . . . @ . @
. . . . @ . O
. . O . @ . @
. . O @ O . O
. O O @ @ O @

and the game declares @ as the winner: "Player @ wins."


Protocol
--------

To each strategy, this program feeds their standard input with the
player they're playing as, as well as the state of the board. It's a
single line where the first character is the player, a white space, 42
characters representing the board and a new line.

The player character is either `@' or `O'.

A board character is either `.', `@', or `O'.

The sequence of characters on the board scans the board from top left
to bottom right. So for example, the board

1 2 3 4 5 6 7
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . O . .
. . . . @ . .

will be received by player @ (the next to play) as

@ ................................O......@..

The strategy has to read the whole line from input and send to the
standard output the column, from 1 to 7, where it wants to place its
piece. So, for example, if @ wants to place its piece in column 7, it
sends

7

a single integer, terminated by a new line. Then the game will send to
player O is the board

1 2 3 4 5 6 7
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . O . .
. . . . @ . @

as the message

O ................................O......@.@

Each strategy must read the game state and write their move in a never
ending loop.


Strategy examples
-----------------

The directory `players/' has example strategies written in Python and
Scheme (with the Scheme implementation called Guile). A strategy can
be written in any programming language, as long as it respects the
protocol.


Usage
-----

To play a game, run this program (`fiar.py') with two arguments, each
implementing the protocol defined earlier. For example, the command

./fiar.py -v players/random_strategy.scm players/random_strategy.py

will make two random strategies face each other, and the switch `-v'
will ensure the boards will be printed.


Problems
--------

* The game is frozen!

A common problem when writing a strategy happens when sending the
column response: the game will freeze. This usually means that the
strategy's output stream is buffered and has to be flushed.

"""

import argparse
import subprocess
import sys
from typing import Literal

EMPTY = "."
PLAYER1 = "@"
PLAYER2 = "O"
OUTER = "?"
MIN_MOVE_VALUE = 1
MAX_MOVE_VALUE = 7
ALL_SQUARES = tuple(s for s in range(10, 62) if MIN_MOVE_VALUE <= s % 9 <= MAX_MOVE_VALUE)
TOP_SQUARES = range(10, 18)
ALL_MOVES = range(MIN_MOVE_VALUE, MAX_MOVE_VALUE + 1)

nw = -10
no = -9
ne = -8
we = -1
ea = 1
sw = 8
so = 9
se = 10


def opponent(player: Literal["@", "O"]) -> Literal["@", "O"]:
    """Return the oponent of a given `player`."""
    return PLAYER1 if player == PLAYER2 else PLAYER2


def make_board() -> str:
    """Create the game board."""
    return "".join(EMPTY if s in ALL_SQUARES else OUTER for s in range(72))


def print_board(board: str) -> str:
    """Print the game board and return the board itself."""
    print("1 2 3 4 5 6 7")
    for row in range(1, 7):
        for column in range(1, 8):
            print(f"{board[row * 9 + column]} ", end="")
        print()
    return board


def is_valid(move: int) -> bool:
    """Check if a given `move` is valid."""
    return isinstance(move, int) and MAX_MOVE_VALUE <= move <= MAX_MOVE_VALUE


def is_legal(move: int, board: str) -> int | None:
    """Check if the move is legal and return the square where the piece will be placed."""
    return find_empty_square(move, board)


def is_any_legal_move(board: str) -> bool:
    """Check if there are any legal moves left."""
    return any(board[s] == EMPTY for s in TOP_SQUARES)


def find_empty_square(column: int, board: str) -> int | None:
    """Find the empty square in a given `column`."""
    square = 54 + column
    while board[square] != OUTER:
        if board[square] == EMPTY:
            return square
        square += no
    return None


def make_move(move: int, player: Literal["@", "O"], board: str) -> tuple[str, int | None]:
    """Make a given `move` and returns a tuple of the new board and the square where the piece was placed."""
    empty_square = find_empty_square(move, board)
    return (
        str(piece if square != empty_square else player for square, piece in enumerate(board)),
        empty_square,
    )


def is_four_in_a_row(square: int, board: str) -> bool:
    """Check for the presence of four pieces in a row around a given `square`."""
    piece = board[square]

    def test_row(dir1: int, dir2: int) -> bool:
        def test_direction(direction: int) -> int:
            count = 0
            s = square + direction
            while board[s] == piece:
                count += 1
                s += direction
            return count

        return test_direction(dir1) + test_direction(dir2) >= 3

    return any(test_row(*d) for d in ((no, so), (ea, we), (ne, sw), (se, nw)))


def player_squares(player: Literal["@", "O"], board: str) -> tuple[int, ...]:
    """Get all squares that belongs to a given `player`."""
    return tuple(s for s in ALL_SQUARES if board[s] == player)


def board_to_string(board: str) -> str:
    """Convert the board to a string."""
    return "".join(board[s] for s in ALL_SQUARES)


class Strategy(subprocess.Popen):
    """Class for the external program that implements the strategy logic."""

    def __init__(self, filename: str) -> None:
        subprocess.Popen(
            [filename],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

    def get_move(self, player: Literal["@", "O"], board: str) -> int:
        """Get the move of the strategy."""
        print(f"{player} {board_to_string(board)}", file=self.stdin, flush=True)
        if self.stdout is not None:
            return int(self.stdout.readline())
        else:
            print("No stdout set.", file=self.stderr, flush=True)
            self.kill()
            sys.exit(1)

    def __exit__(self, _exc_type, _exc_value, _traceback):
        self.kill()


def four_in_a_row(strategy1: Strategy, strategy2: Strategy, is_print: bool = True) -> None:
    """Play a game of four in a row between two strategies."""

    def play_turn(player: Literal["@", "O"], board: str) -> tuple[Literal[-1, 0, 1], str]:
        if is_print:
            print_board(board)
        if is_any_legal_move(board):
            strategy = strategy1 if player == PLAYER1 else strategy2
            move = strategy.get_move(player, board)
            if move is not None and is_valid(move) and is_legal(move, board):
                new_board, square = make_move(move, player, board)
                if square is not None and is_four_in_a_row(square, new_board):
                    return 1 if player == PLAYER1 else -1, new_board
                else:
                    return play_turn(opponent(player), new_board)
            else:
                return play_turn(player, board)
        else:
            return 0, board

    score, board = play_turn(PLAYER1, make_board())
    if is_print:
        print_board(board)
    if score == 0:
        print("Draw.")
    else:
        print(f"Player {PLAYER1 if score > 0 else PLAYER2} wins.")


parser = argparse.ArgumentParser(description="Plays a game of four-in-a-row.")
parser.add_argument("player1", help="First player to move, represented by @.")
parser.add_argument("player2", help="Second player to move, represented by O.")
parser.add_argument("-v", "--verbose", help="print boards", action="store_true")
args = parser.parse_args()

with Strategy(args.player1) as strategy1, Strategy(args.player2) as strategy2:
    four_in_a_row(strategy1, strategy2, args.verbose)
