(define (domain exploration-game)
    (:requirements ; list of requirements for the planner: https://planning.wiki/ref
        :strips :typing :negative-preconditions
    )
    (:types location player item choice)

    (:predicates
        ; player p has the item i
        (has ?p - player ?i - item)

        ; player p is at location l
        (is_at ?p - player ?l - location)

        ; it is always possible to move from location src to location dst
        (connected ?src - location ?dst - location)

        ; it is possible to move from location src to location dst if we have item i
        (connected_if ?src - location ?dst - location ?i - item)

        ; at location l, it is possible to collect item i
        (possible_collect ?l - location ?i - item)

        ; at location l, it is possible to collect item i if we have item req
        (possible_collect_if ?l - location ?i - item ?req - item)

        ; at location l, it is possible to collect item i if we have item req1 and item req2
        (possible_collect_if_2 ?l - location ?i - item ?req1 - item ?req2 - item)

        ; the choice c offers the possibility to collect the item i
        (offers ?c - choice ?i - item)

        ; the choice c has been made by the player p
        (made_by ?c - choice, ?p - player)

        ; at location l, it is possible to make the choice c
        (possible_choice ?l - location ?c - choice)
    )

    ; player p moves from location src to location dst
    (:action move
        :parameters (?p - player ?src - location ?dst - location)
        :precondition (and
            (connected ?src ?dst)
            (is_at ?p ?src)
        )
        :effect (and
            (not (is_at ?p ?src))
            (is_at ?p ?dst)
        )
    )

    ; player p moves from location src to location dst by using the item i
    (:action move_using
        :parameters (?p - player ?src - location ?dst - location ?i - item)
        :precondition (and
            (connected_if ?src ?dst ?i)
            (is_at ?p ?src)
            (has ?p ?i)
        )
        :effect (and
            (not (is_at ?p ?src))
            (is_at ?p ?dst)
        )
    )

    ; player p, at location l, collects item i
    (:action collect
        :parameters (?p - player ?l - location ?i - item)
        :precondition (and
            (possible_collect ?l ?i)
            (is_at ?p ?l)
        )
        :effect (and
            (has ?p ?i)
        )
    )

    ; player p, at location l, collects item i by using item req
    (:action collect_using_1
        :parameters (?p - player ?l - location ?i - item ?req - item)
        :precondition (and
            (possible_collect_if ?l ?i ?req)
            (is_at ?p ?l)
            (has ?p ?req)
        )
        :effect (and
            (has ?p ?i)
        )
    )

    ; player p, at location l, collects item i by using item req1 and item req2
    (:action collect_using_2
        :parameters (?p - player ?l - location ?i - item ?req1 - item ?req2 - item)
        :precondition (and
            (possible_collect_if_2 ?l ?i ?req1 ?req2)
            (is_at ?p ?l)
            (has ?p ?req1)
            (has ?p ?req2)
        )
        :effect (and
            (has ?p ?i)
        )
    )

    ; player p, at location l, makes the choice c, by collecting the item i
    (:action make_choice
        :parameters (?p - player ?l - location ?c - choice ?i - item)
        :precondition (and
            (possible_choice ?l ?c)
            (is_at ?p ?l)
            (not (made_by ?c, ?p))
            (offers ?c ?i)
        )
        :effect (and
            (made_by ?c, ?p)
            (has ?p ?i)
        )
    )
)
