types
    turn : FiniteRange(0,1)
    ahit : FiniteRange(0,1)
    bhit : FiniteRange(0,1)
end

turn = 0
ahit = 0
bhit = 0
while ahit == 0 && bhit == 0:
    if turn == 0:
        ahit = Bernoulli(pa)
    else:
        bhit = Bernoulli(pb)
    end
    
    turn = 1 - turn
end
