# FROM: Bayesian Inference using Data Flow Analysis; Claret et al.
# Compute uniform probability between 0 and bound - 1

types
    bound : FiniteRange(500,500)
    n : FiniteRange(1,1000)
    f : FiniteRange(0,1)
    g : FiniteRange(0,1500)
end

bound = 500
g = bound
while g >= bound:
    n = 1
    g = 0
    while n < bound:
        n = 2*n
        f = Bernoulli(1/2)
        if f == 1:
            g = 2*g
        else:
            g = 2*g+1
        end
    end
end
