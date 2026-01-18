import math
import numpy as np
from sympy import primerange, factorint, gcd
from math import isqrt


def quadratic_sieve(n, b, interval):
    # Create the factor base: small primes up to the bound b
    factor_base = [-1] + list(primerange(2, b))  # Include -1 in the factor base to handle negative Q(x) values
    print("Factor base:", factor_base)

    # Store (x, q(x), factorization) for b-smooth values
    smooth_relations = []

    x0 = math.isqrt(n)  # Start searching around sqrt(n)

    # Loop over values around x0
    for i in range(-interval, interval + 1):
        x = x0 + i
        qx = x * x - n

        fac = factorint(qx)  # factor qx into its prime factors
        primes_in_qx = list(fac.keys())

        # Check if q(x) is b-smooth
        if all(p in factor_base for p in primes_in_qx):
            smooth_relations.append((x, qx, fac))
    print(f"\nFound {len(smooth_relations)} smooth relations\n")

    if len(smooth_relations) <= len(factor_base):
        print("Not enough relations — increase B or interval.")

    # Build exponent matrix modulo 2
    exp_matrix = []
    for (x, qx, fac) in smooth_relations:
        row = []
        for p in factor_base:
            # Store exponent parity (even/odd)
            e = fac.get(p, 0) % 2
            row.append(e)
            exp_matrix.append(row)
            print(f"x = {x}, exponents mod 2 = {row}")

    # Convert exponent matrix to a NumPy array
    # Reduce everything modulo 2 explicitly
    m = np.array(exp_matrix, dtype=int) % 2

    rows, cols = m.shape
    print(f"x ={x}, Q(x)= {qx}, factors= {fac}")

    # We transpose the matrix so that columns correspond to relations
    # This makes it easier to find dependencies
    A = m.T.copy()

    pivot_cols = []  # Columns with pivots
    r = 0  # Current pivot row

    # Gaussian elimination modulo 2
    for c in range(A.shape[1]):  # Iterate over columns
        for i in range(r, A.shape[0]):  # Search for a pivot
            if A[i, c] == 1:
                # Swap rows to move pivot into position
                A[[r, i]] = A[[i, r]]
                pivot_cols.append(c)

                # Eliminate all other 1s in this column
                for j in range(A.shape[0]):
                    if j != r and A[j, c] == 1:
                        A[j] ^= A[r]  # XOR operation (addition mod 2)
                r += 1
                break

    # Columns without pivots correspond to dependencies
    free_cols = [c for c in range(A.shape[1]) if c not in pivot_cols]

    for fc in free_cols:
        # Dependency vector
        v0 = np.zeros(A.shape[1], dtype=int)
        v0[fc] = 1

        # Compute remaining entries using pivot rows
        for i, pc in enumerate(pivot_cols):
            v0[pc] = A[i, fc]

        x_val = 1
        y_val = 1

        # Combine relations according to dependency vector
        for i in range(len(smooth_relations)):
            if v0[i] == 1:
                # Multiply x values
                x_val *= smooth_relations[i][0]

                # Multiply q(x) values
                y_val *= smooth_relations[i][1]

        x_val %= n  # Reduce x modulo n
        y_val = abs(y_val)  # y_val should be a perfect square

        # Check if y_val is a perfect square
        if not isqrt(y_val):
            continue
        y_val = math.isqrt(y_val)
        print(f"x: {x_val}, y: {y_val}")
        print("gcd:", gcd(x_val + y_val, n), gcd(x_val - y_val, n))

        # Try to extract a nontrivial factor
        if 1 < gcd(x_val + y_val, n) < n:
            print("Factor found:", gcd(x_val + y_val, n), n // gcd(x_val + y_val, n))
            return gcd(x_val + y_val, n)
        if 1 < gcd(x_val - y_val, n) < n:
            print("Factor found:", gcd(x_val - y_val, n), n // gcd(x_val - y_val, n))
            return gcd(x_val - y_val)

    # If no factor was found
    print("No nontrivial factor found.")
    return 0