#lang typed/racket
(require typed/json)

(define x (file->string "test.json"))

(: testJson (-> String String))
(define (testJson expr)
  (match (string->jsexpr expr)
    [(hash-table ('declarations a) ('functions b) ('types c)) "matched to json"]
    [other "fail"]))

(testJson x)