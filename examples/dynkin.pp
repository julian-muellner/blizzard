# FROM: Coupling Proofs Are Probabilistic Product Programs, CAV'17
# PSI Implementation: https://github.com/eth-sri/psi/blob/master/test/cards.psi


types
    x : FiniteRange(1,109)
    y : FiniteRange(1,10)
end

x = DiscreteUniform(1,10)
while x < 100:
    y = DiscreteUniform(1,10)
    x = x + y
end
