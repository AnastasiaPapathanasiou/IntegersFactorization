import math
import sympy as sp
from sympy import Poly, ZZ, gcd, sqrt
from fpylll import IntegerMatrix, LLL


def coppersmith_method(N, p0, eps=0.5, h=4):
    # Define a symbolic variable x
    x = sp.Symbol('x')

    # Define the polynomial f, the root is x0 = p - p0
    f = x + p0

    # Lattice dimension n = h * d = h (since d = 1)
    k = 2*h

    # Coppersmith bound on the unknown root x0:
    # From Theorem 1 of the paper: |x0| < (1/2) * N^(1/4 - epsilon)
    X = int(N ** (0.25 - eps)/ (2*sqrt(2)))

    # Build shifted polynomials
    fh = f**h
    polys = []
    for j in range(h+1):
        q1 = (f ** j) * (N ** (h - j))
        p1 = Poly(q1, x, domain=ZZ)
        if j != 0:
            q2 = x**j * fh
            p2 = Poly(q2, x, domain=ZZ)
            polys.append(p2)
        polys.append(p1)
        # print(f"p1: {p1}")
        # print(f"p2: {p2}")

    Mrows = []
    for poly in polys:
        coeffs = poly.all_coeffs()
        coeffs = [int(val) for val in coeffs]
        coeffs = (k+1 - len(coeffs))*[0] + coeffs
        Mrows.append(coeffs)
    M = IntegerMatrix.from_matrix(Mrows)

    return M
    # Apply LLL basis reduction to M
    MLLL = LLL.reduction(M)
    #
    # # Reconstruct C(x) from the first row of the reduced basis
    # C = 0
    # for col_idx in range(n):
    #     coeff = M[0, col_idx] // (X ** col_idx)
    #     C += coeff * (x ** col_idx)
    #
    # C = Poly(C, x, domain=ZZ)
    #
    # # Find integer roots of C(x) over Z
    # roots = C.ground_roots()
    # print(roots)
    #
    # for x0_candidate in roots:
    #     x0 = int(x0_candidate)
    #
    #     if abs(x0) > X:
    #         continue
    #
    #     # Recover candidate prime: p = p0 + x0
    #     p_candidate = p0 + x0
    #
    #     # Verify factorization
    #     if p_candidate > 1 and N % p_candidate == 0:
    #         p = p_candidate
    #         q = N // p
    #         return int(p), int(q)

    return None


