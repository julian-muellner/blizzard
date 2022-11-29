from typing import List

from symengine.lib.symengine_wrapper import Expr, Symbol, One, Zero, Rational


def float_to_rational(expr: Expr):
    return Rational(str(expr))


def get_monoms(poly: Expr, constant_symbols=None, with_constant=False, zero=Zero(), one=One()):
    """
    For a given polynomial returns a list of its monomials with separated coefficients - (coeff, monom).
    The polynomial is assumed to be in all symbols it contains minus constant_symbols.
    The monomial 1 is only included if with_constant is true.
    """
    if constant_symbols is None:
        constant_symbols = set()

    monoms = []
    constant = zero
    terms = poly.args if poly.is_Add else [poly]
    for term in terms:
        if not term.free_symbols.difference(constant_symbols):
            constant += term
            continue

        coeff = one
        monom = one
        parts = term.args if term.is_Mul else [term]
        for part in parts:
            if part.free_symbols.difference(constant_symbols):
                monom *= part
            else:
                coeff *= part
        monoms.append((coeff, monom))

    if with_constant and constant != 0:
        monoms.append((constant, One()))
    return monoms

