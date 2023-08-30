# FROM: https://arxiv.org/pdf/math/0110143.pdf
# Similar example used in: Coupling Proofs Are Probabilistic Product Programs, CAV'17, PSI Implementation: https://github.com/eth-sri/psi/blob/master/test/cards.psi

types
    x1 : FiniteRange(1,59)
    x2 : FiniteRange(1,59)
    y : FiniteRange(1,10)
    z : FiniteRange(0,1)
end

x1 = DiscreteUniform(1,10)
x2 = DiscreteUniform(1,10)
while (x1 < 49) || (x2 < 49):
    y = DiscreteUniform(1,10)
    if x1 == x2:
        x1 = x1 + y
        x2 = x2 + y
    else:
        if x1 < x2:
            x1 = x1 + y
        else:
            x2 = x2 + y
        end
    end
end

z = 0
if x1 == x2:
    z = 1
end
