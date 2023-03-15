#!/usr/bin/env guile -s
!#

; Copyright (C) 2023  Diogo F. S. Ramos and UFABC Dojo Members

(use-modules (ice-9 rdelim)
             (srfi srfi-1))

(define empty #\.)
(define all-moves (iota 7 1))

(define (random-ref list)
  (list-ref list (random (length list))))

(define (valid? move board)
  (char=? empty (string-ref board (1- move))))

(define (random-strategy board)
  (random-ref (filter (lambda (move) (valid? move board))
                      all-moves)))

(set! *random-state* (random-state-from-platform))
(while #t
  (write-line (random-strategy (substring (read-line) 2)))
  (force-output))
