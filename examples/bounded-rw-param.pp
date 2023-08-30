
types
    x : FiniteRange(-2,12)
    f : FiniteRange(0,1)
    z : FiniteRange(1,3)
end

x = 4
while x > 0 && x < 5:
    f = Bernoulli(p)
    if f == 1:
        z = DiscreteUniform(1,3)
        x = x + z
    else:
        f = Bernoulli(q)
        if f == 1:
            x = x - 2
        else:
            x = x - 3
        end
    end
end
