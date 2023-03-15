#!/usr/bin/env guile -s
!#

; Copyright (C) 2023  Diogo F. S. Ramos
;
; This program is free software; you can redistribute it and/or modify
; it under the terms of the GNU General Public License as published by
; the Free Software Foundation; either version 2 of the License.

(use-modules (ice-9 rdelim)
             (srfi srfi-1)
             (ice-9 format)
             (ice-9 receive))

(define empty 0)
(define player1 1)
(define player2 2)
(define outer 3)
(define all-moves (iota 7 1))
(define all-squares
  (filter (lambda (square)
            (and (<= 10 square 61)
                 (<= 1 (modulo square 9) 7)))
          (iota 72)))

(define nw -10) (define no -9) (define ne -8)
(define we -1)                 (define ea 1)
(define sw 8)   (define so 9)  (define se 10)

(define winning-value +inf.0)
(define losing-value -inf.0)

(define (name-of piece)
  (string-ref ".@O?" piece))

(define (piece-of name)
  (string-index ".@O?" name))

(define (make-board)
  (let ((board (make-vector 72 outer)))
    (for-each (lambda (square)
                (vector-set! board square empty))
              all-squares)
    board))

(define (copy-board board)
  (vector-copy board))

(define board-ref
  (make-procedure-with-setter (lambda (board square)
                                (vector-ref board square))
                              (lambda (board square piece)
                                (vector-set! board square piece))))

(define (read-board-from-string string)
  (define (square->index s)
    (- s 10 (* 2 (quotient (- s 9) 9))))
  (let ((board (make-board)))
    (for-each (lambda (square)
                (set! (board-ref board square)
                      (piece-of (string-ref string
                                            (square->index square)))))
              all-squares)
    board))

(define (move->bottom-square move)
  (+ move 54))

(define (move->top-square move)
  (+ move 9))

(define (make-move move player board)
  (do ((square (move->bottom-square move) (+ square no)))
      ((eqv? (board-ref board square) empty)
       (set! (board-ref board square) player)
       board)))

(define (print-board board)
  (format #t "~2&     ~{~a~^ ~}" (iota 7 1))
  (do ((row 1 (1+ row)))
      ((< 6 row))
    (format #t "~&  ~2d "(* row 9))
    (do ((column 1 (1+ column)))
        ((< 7 column))
      (format #t "~c " (name-of (board-ref board
                                           (+ (* row 9) column))))))
  (format #t "~2&")
  board)

(define (valid? move)
  (and (integer? move) (<= 1 move 7)))

(define (legal? move board)
  (eqv? (board-ref board (move->top-square move))
        empty))

(define (legal-moves board)
  (filter (lambda (move) (legal? move board))
          all-moves))

(define (count-equal-squares square dir piece board)
  (if (eqv? (board-ref board square) piece)
      (1+ (count-equal-squares (+ square dir) dir piece board))
      0))

(define (row-size dir1 dir2 square board)
  (let ((piece (board-ref board square)))
    (+ 1
       (count-equal-squares (+ square dir1) dir1 piece board)
       (count-equal-squares (+ square dir2) dir2 piece board))))

(define (row-size-score square board)
  (- (+ (row-size no so square board)
        (row-size ea we square board)
        (row-size nw se square board)
        (row-size ne sw square board))
     3))

(define (longest-row square board)
  (max (row-size no so square board)
       (row-size ea we square board)
       (row-size nw se square board)
       (row-size ne sw square board)))

(define (player-squares player board)
  (filter (lambda (square)
            (eqv? player (board-ref board square)))
          all-squares))

(define (player-longest-row player board)
  (fold max 0 (map (lambda (square)
                     (longest-row square board))
                   (player-squares player board))))

(define (player-row-size-score player board)
  (define (sum list) (fold + 0 list))
  (- (sum (map (lambda (square) (row-size-score square board))
               (player-squares player board)))
     (sum (map (lambda (square) (row-size-score square board))
               (player-squares (opponent player) board)))))

(define (opponent player)
  (if (eqv? player1 player)
      player2
      player1))

(define (game-ended? board)
  (or (null? (legal-moves board))
      (< 3 (player-longest-row player1 board))
      (< 3 (player-longest-row player2 board))))

(define (final-value player board)
  (cond ((< 3 (player-longest-row player board))
         winning-value)
        ((< 3 (player-longest-row (opponent player) board))
         losing-value)
        (else 0)))

(define (minimax player board ply eval-proc)
  (define (pick-best-move moves)
    (if (null? moves)
        (values #f #f)
        (receive (best-val best-move)
            (pick-best-move (cdr moves))
          (let* ((move (car moves))
                 (board2 (make-move move
                                    player
                                    (copy-board board)))
                 (val (- (minimax (opponent player)
                                  board2
                                  (1- ply)
                                  eval-proc))))
            (if (or (not best-val)
                    (< best-val val))
                (values val move)
                (values best-val best-move))))))
  (cond ((zero? ply)
         (eval-proc player board))
        ((game-ended? board)
         (final-value player board))
        (else
         (pick-best-move (legal-moves board)))))

(define (minimax-strategy ply eval-proc)
  (lambda (player board)
    (receive (value move)
        (minimax player board ply eval-proc)
      move)))

(let ((strategy (minimax-strategy 5 player-row-size-score)))
  (while #t
    (let* ((line (read-line))
           (player (piece-of (string-ref line 0)))
           (board (read-board-from-string (substring line 2))))
      (write-line (strategy player board))
      (force-output))))
