#!env janet

# Copyright (C) 2023  Diogo F. S. Ramos and UFABC Dojo Members

(def EMPTY ".")
(def INVALID_MOVE -1)
(def ALL_MOVES (range 1 8))

(defn legal? [move board]
  (let [square (string/from-bytes (get board (- move 1)))]
    (compare= square EMPTY)))

(defn select-random [rng legal-moves]
  (let [index (math/rng-int rng (- (length legal-moves) 1))]
    (legal-moves index)))

(defn random-strategy [board]
  (let [legal-moves (filter (fn [move] (legal? move board)) ALL_MOVES)
        rng (math/rng)]
    (if (empty? legal-moves)
      INVALID_MOVE
      (select-random rng legal-moves))))

(while true
  (let [input (string/trim (file/read stdin :line))]
    (print (random-strategy (string/slice input 2)))))
