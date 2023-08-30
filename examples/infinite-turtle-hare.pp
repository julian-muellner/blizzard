
types
    delta : FiniteRange(-3,20)
    y : FiniteRange(0, 1)
    winner : FiniteRange(0, 1)
    z : FiniteRange(1, 5)
end

delta = 2
while (delta > 0) && (delta < 5):
    y = Bernoulli(p)
    delta = delta + 1
    if y == 1:
        z = DiscreteUniform(1,3)
        delta = delta - z
    end
    y = 0
    z = 1
end

if delta <= 0:
    winner = 0 # hare wins
else:
    winner = 1 # turtle wins
end
