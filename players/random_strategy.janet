#!/usr/bin/env janet

# Copyright (C) 2023  Diogo F. S. Ramos and UFABC Dojo Members

(def EMPTY ".")
(def ALL_MOVES (range 1 8))
(def RNG (math/rng))

(defn legal? [move board]
  (let [square (string/from-bytes (get board (- move 1)))]
    (compare= square EMPTY)))

(defn select-random [legal-moves]
  (let [index (math/rng-int RNG (- (length legal-moves) 1))]
    (legal-moves index)))

(defn random-strategy [board]
  (let [legal-moves (filter (fn [move] (legal? move board)) ALL_MOVES)]
    (select-random legal-moves)))

(defn main [args]
  (while true
    (let [input (string/trim (file/read stdin :line))]
      (print (random-strategy (string/slice input 2)))
      (file/flush stdout))))
