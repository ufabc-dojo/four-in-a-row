# Four In A Row

This program implements the game Four In A Row, to be played by two external programs (strategies).

The objective of the game is to place your pieces in a row of four pieces. The row can be horizontal, vertical, or diagonal.

The board is a matrix of 6 by 7 and each player chooses the column to place their piece. A piece will rest at the bottom of the board or on top of another piece.

The following is a representation of an empty board. Each `.` marks empty space and the top numbers mark the columns.

```
1 2 3 4 5 6 7
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
```

There're two players: `@` and `O`. The first player to move is `@`, then `O`. Each player places their pieces in turns. So after two turns, the board might look like as:

```
1 2 3 4 5 6 7
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . O . .
. . . . @ . .
```

where player `@` placed their piece at column 5, and then player `O` too placed their piece in column 5.

A game ends when four pieces are placed in a row, as in

```
1 2 3 4 5 6 7
. . . . @ . O
. . . . @ . @
. . . . @ . O
. . O . @ . @
. . O @ O . O
. O O @ @ O @
```

and the game declares `@` as the winner: "Player @ wins."

## Protocol

To each strategy, this program feeds their standard input with the player they're playing as, as well as the state of the board. It's a single line where the first character is the player, a white space, 42 characters representing the board and a new line.

The player character is either `@` or `O`.

A board character is either `.`, `@`, or `O`.

The sequence of characters on the board scans the board from top left to bottom right. So for example, the board

```
1 2 3 4 5 6 7
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . O . .
. . . . @ . .
```

will be received by player `@` (the next to play) as:

```
@ ................................O......@..
```

The strategy has to read the whole line from input and send to the
standard output the column, from 1 to 7, where it wants to place its
piece. So, for example, if `@` wants to place its piece in column 7, it
sends

```
7
```

a single integer, terminated by a new line. Then the game will send to
player `O` is the board

```
1 2 3 4 5 6 7
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . O . .
. . . . @ . @
```

as the message

```
O ................................O......@.@
```

Each strategy must read the game state and write their move in a never ending loop.

## Strategy examples

The directory `players/` has example strategies written in Python and Scheme (with the Scheme implementation called Guile). A strategy can be written in any programming language, as long as it respects the protocol.

## Usage

To play a game, run this program (`fiar.py`) with two arguments, each implementing the protocol defined earlier. For example, the command

```bash
./fiar.py -v players/random_strategy.scm players/random_strategy.py
```

will make two random strategies face each other, and the switch `-v` will ensure the boards will be printed.

## Common Problems

### The game is frozen!

A common problem when writing a strategy happens when sending the column response: the game will freeze. This usually means that the strategy's output stream is buffered and has to be flushed.
