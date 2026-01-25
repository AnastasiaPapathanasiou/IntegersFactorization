import math


def fermat_algorithm(n, s_bound):
    # Quick check for even n (trivial factor)
    if n % 2 == 0:
        return 2, n // 2

    # Compute the integer square root of N
    # This gives the larger integer x0 such that x0^2 <= N
    x0 = math.isqrt(n)

    # If x0^2 is strictly smaller than N, increment x0 so that x0 = ceil(sqrt(N))
    # Fermat's method requires starting from the smallest x >= sqrt(N)
    if x0 * x0 < n:
        x0 = x0 + 1  # ceil(sqrt(N))

    # Iterate over successive values of x, bounded by s_bound
    for i in range(s_bound):
        # Current value of x in the iteration
        xi = x0 + i
        yi2 = xi * xi - n

        if yi2 >= 0:
            # Compute the integer square root of yi2
            y = math.isqrt(yi2)

            # Check whether yi2 ia a perfect square
            # If y^2 = yi2 then N = (x+y)(x-y)
            if y * y == yi2:
                # Compute the factors of N
                p = xi + y
                q = xi - y

                # Return the factorization
                return p, q

    return None


