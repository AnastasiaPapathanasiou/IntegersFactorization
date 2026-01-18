import math
import numpy as np
from sympy import primerange, factorint, gcd
from math import isqrt


def quadratic_sieve(n, b, interval):

    # we create the factor base: a list of small primes up to the bound B
    factor_base = [-1] + list(primerange(2, b))  # we include -1 in the factor base to handle negative Q(x) values
    print("Factor base:", factor_base)

    # we compute Q(x) = x² - N for a range of x values centered around sqrt(N), and check which Q(x) are B-smooth
    smooth_relations = []
    x0 = math.isqrt(n)
    # loop over values around x0
    for i in range(-interval, interval + 1):
        x = x0 + i
        qx = x * x - n

        fac = factorint(qx)  # factor Qx into its prime factors
        primes_in_qx = list(fac.keys())
        # we check if all the primes in the factorization belong to the factor base

        if all(p in factor_base for p in primes_in_qx):
            smooth_relations.append((x, qx, fac))
    print(f"\nFound {len(smooth_relations)} smooth relations\n")

    if len(smooth_relations) <= len(factor_base):
        print("Not enough relations — increase B or interval.")


    exp_matrix = []
    for (x, qx, fac) in smooth_relations:
        row = []
        for p in factor_base:
            e = fac.get(p, 0) % 2
            row.append(e)
            exp_matrix.append(row)
            print(f"x = {x}, exponents mod 2 = {row}")

    m = np.array(exp_matrix, dtype=int) % 2
    rows, cols = m.shape
    print(f"x ={x}, Q(x)= {qx}, factors= {fac}")

    A = m.T.copy()
    pivot_cols = []
    r = 0
    for c in range(A.shape[1]):
        for i in range(r, A.shape[0]):
            if A[i, c] == 1:
                A[[r, i]] = A[[i, r]]
                pivot_cols.append(c)
                for j in range(A.shape[0]):
                    if j != r and A[j, c] == 1:
                        A[j] ^= A[r]
                r += 1
                break

    free_cols = [c for c in range(A.shape[1]) if c not in pivot_cols]

    for fc in free_cols:
        v0 = np.zeros(A.shape[1], dtype=int)
        v0[fc] = 1
        for i, pc in enumerate(pivot_cols):
            v0[pc] = A[i, fc]

        x_val = 1
        y_val = 1

        for i in range(len(smooth_relations)):
            if v0[i] == 1:
                x_val *= smooth_relations[i][0]
                y_val *= smooth_relations[i][1]

        x_val %= n
        y_val = abs(y_val)

        if not isqrt(y_val):
            continue

        y_val = math.isqrt(y_val)
        print(f"x: {x_val}, y: {y_val}")
        print("gcd:", gcd(x_val + y_val, n), gcd(x_val - y_val, n))


        if 1 < gcd(x_val + y_val, n) < n:
            print("Factor found:", gcd(x_val + y_val, n), n // gcd(x_val + y_val, n))
            return gcd(x_val+ y_val, n)
        if 1 < gcd(x_val - y_val, n) < n:
            print("Factor found:", gcd(x_val - y_val, n), n // gcd(x_val -y_val, n))
            return gcd(x_val - y_val)

    print("No nontrivial factor found.")
    return 0
