#!/usr/bin/env python3

# Copyright (C) 2023  Diogo F. S. Ramos and UFABC Dojo Members

import random

EMPTY = "."
ALL_MOVES = range(1, 8)


def is_legal(move: int, board: str) -> bool:
    """Check if `move` is legal."""
    return board[move - 1] == EMPTY


def random_strategy(board: str) -> int:
    """Make a random move."""
    return random.choice([move for move in ALL_MOVES if is_legal(move, board)])


while True:
    print(random_strategy(input()[2:]))
