(ns tensora.demo
  (:require [clojure.string :as str]))

(defn word-freq
  "Count the words in text, most frequent first."
  [text]
  (->> (str/split (str/lower-case text) #"\W+")
       (remove str/blank?)
       frequencies
       (sort-by val >)))

(comment
  (word-freq "the cat and the hat and the bat")
  ;; => (["the" 3] ["and" 2] ["cat" 1] ["hat" 1] ["bat" 1])
  )
