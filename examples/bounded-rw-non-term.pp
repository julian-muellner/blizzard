
types
    x : FiniteRange(-1,12)
    f : FiniteRange(0,1)
    term : FiniteRange(0,1)
    z : FiniteRange(1,3)
end

x = 4
term = Bernoulli(9/10)
while x > 0 && x < 5:
    if term == 1:
        f = Bernoulli(5/10)
        if f == 1:
            z = DiscreteUniform(1,3)
            x = x + z
        else:
            x = x - 2
        end
    else:
        observe 1 < 0
    end
end
