import math
import sympy as sp
from sympy import Poly, ZZ, gcd, sqrt
from sympy import Integer
from fpylll import IntegerMatrix, LLL


def coppersmith_method(N, p0, h=7):
    # Define a symbolic variable x
    x = sp.Symbol('x')

    # Define the polynomial f, the root is x0 = p - p0
    f = x + p0

    # Lattice dimension : (h+1) x (h+1) square matrix (d=1, so n = d*h + 1 = h+1)
    k = h + 1

    # Bound on the unknown root: |x0| = |p - p0| < N^(1/4)
    X = int(math.isqrt(math.isqrt(int(N)))) + 1
    print("X =", X)

    # Build shifted polynomials: g_j(x) = f(x)^j * N^(h-j), j = 0,...,h
    # Each g_j satisfies g_j(x0) = 0 (mod N^j) since f(x0) = p | N
    polys = []
    for j in range(h + 1):
        q1 = (x + p0) ** j * (N ** (h - j))
        p1 = Poly(q1, x, domain=ZZ)
        polys.append(p1)

    # Build lattice matrix M with column scaling X^i
    Mrows = []
    for poly in polys:
        coeffs_dict = poly.as_dict()
        row = []
        for i in range(k):
            c = int(coeffs_dict.get((i,), 0))
            row.append(c * (X ** i))
        Mrows.append(row)
    M = IntegerMatrix.from_matrix(Mrows)
    print("Lattice matrix built, size:", M.nrows, "x", M.ncols)

    # Apply LLL basis reduction to M
    MLLL = LLL.reduction(M)

    # Reconstruct C(x) from the first row of the reduced basis
    # Use exact integer arithmetic (sympy Integer + divmod) to reverse the X^i scaling.
    C = 0
    for i in range(MLLL.ncols):
        coeff, _ = divmod(Integer(MLLL[0, i]), Integer(X) ** i)
        C += int(coeff) * (x ** i)

    C = Poly(C, x, domain=ZZ)
    print("Reduced polynomial:", C)

    # Find integer roots of C(x) over Z
    roots = C.ground_roots()
    print("Roots of C(x):", roots)

    for x0_candidate in roots:
        x0 = int(x0_candidate)

        if abs(x0) > X:
            continue

        # Recover candidate prime: p = p0 + x0
        p_candidate = p0 + x0
        # Verify factorization

    for x0 in range(-X, X + 1):
        p_candidate = p0 + x0
        if p_candidate > 1 and N % p_candidate == 0:
            p = p_candidate
            q = N // p
            return int(p), int(q)

    return None