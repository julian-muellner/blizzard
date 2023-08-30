# FROM: SPPL

types
    nation : FiniteRange(0,1)
    perfect : FiniteRange(0,1)
    gpa : FiniteRange(0,10)
end

nation = Bernoulli(1/2)
if nation == 0: # US
    perfect = Bernoulli(1/10)
    if perfect == 1:
        gpa = 10
    else:
        gpa = DiscreteUniform(0,9)
    end
else:
    perfect = Bernoulli(15/100)
    if perfect == 1:
        gpa = 4
    else:
        gpa = DiscreteUniform(0,3)
    end
end

#observe ((nation == 0) && (gpa > 3)) || ((8 < gpa) && (gpa < 10))
