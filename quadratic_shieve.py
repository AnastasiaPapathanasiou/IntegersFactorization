import math
import time
from sympy import primerange, isprime, nextprime, factorint, gcd, sqrt
import matplotlib.pyplot as plt


def quadratic_sieve(N, B, interval):

    # we create the factor base: a list of small primes up to the bound B
    b_smooth_primes = [-1] + list(primerange(2, B))  # we include -1 in the factor base to handle negative Q(x) values

    # we compute Q(x) = x² - N for a range of x values centered around sqrt(N), and check which Q(x) are B-smooth
    smooth_relations = []
    x0 = math.isqrt(N)
    # loop over values around x0
    for i in range(-interval, interval + 1):
        x = x0 + i
        x2 = x ** 2
        Qx = x2 - N
        fac = factorint(Qx)  # factor Qx into its prime factors
        primes_in_Qx = list(fac.keys())
        # we check if all the primes in the factorization belong to the factor base
        if all(p in b_smooth_primes for p in primes_in_Qx):
            smooth_relations.append((x, Qx, fac))

    print("Factor Base:", b_smooth_primes)
    print("Compute Qx and check B-smooth:\n")
    for (x, Qx, fac) in smooth_relations:
        if (p in factor_base for p in primerange(B)):
            print(f"x ={x}, Q(x)= {Qx}, factors= {fac}")

    # we build a matrix of exponents modulo 2 for its smooth relation
    exp_matrix = []
    for (x, Qx, fac) in smooth_relations:
        row = []  # each row corresponds to one relation (x, Q(x)), and each column to a prime
        for p in b_smooth_primes:
            # we get the exponent of prime p in the factorization (0 if not present)
            e = fac.get(p, 0) % 2  # modulo 2
            row.append(e)
        exp_matrix.append(row)
        print(f"x = {x}, exponents mod2 = {row}")

    F2 = Integers(2)
    M = matrix(F2, exp_matrix)
    for v0 in M.left_kernel():
        X = [ZZ(v0[i]) * smooth_relations[i][0] for i in range(len(smooth_relations))]
        X = prod([x0 for x0 in X if x0 != 0])
        Y = [ZZ(v0[i]) * smooth_relations[i][1] for i in range(len(smooth_relations))]
        Y = prod([y0 for y0 in Y if y0 != 0])
        Y = sqrt(Y)
        print(f"X: {X}, Y: {Y}, X+Y: {X + Y}, X-Y: {X - Y}, gcd: {gcd(X + Y, N)}, {gcd(X - Y, N)}")


Quadratic_Sieve(227179, 25, 20)