#lang racket


(require json)

(define x (string->jsexpr (file->string "test.json")))

; {"types":[],"declarations":[{"line":1,"type":"int","id":"a"}],"functions":[]}



(define (testJson expr)
  (match expr
    [(hash-table ('declarations a) ('functions b) ('types c)) "matched to json"]
    [other "fail"]))

(testJson x)