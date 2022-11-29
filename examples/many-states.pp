
types
    x : FiniteRange(0,300)
    i : FiniteRange(0,101)
    z : FiniteRange(1,3)
end

i = 0
x = 0
while i < 100:
    z = DiscreteUniform(1,3)
    x = x + z
    i = i + 1
end
