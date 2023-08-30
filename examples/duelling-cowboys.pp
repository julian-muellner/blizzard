# FROM: SPPL

types
    turn : FiniteRange(0,1)
    ahit : FiniteRange(0,1)
    bhit : FiniteRange(0,1)
    stop : FiniteRange(0,1)
end

turn = 0
stop = 0
ahit = 0
bhit = 0
while stop == 0:
    if turn == 0:
        ahit = Bernoulli(pa)
        if ahit == 1:
            stop = 1
        else:
            turn = 1
        end
    else:
        bhit = Bernoulli(pb)
        if bhit == 1:
            stop = 1
        else:
            turn = 0
        end
    end
end
