import math
import time
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


def Fermat_algorithm(N, s_bound):
    # Compute the integer square root of N
    # This gives the larger integer x0 such that x0^2 <= N
    x0 = math.isqrt(N)

    # If x0^2 is strictly smaller than N, increment x0 so that x0 = ceil(sqrt(N))
    # Fermat's method requires starting from the smallest x >= sqrt(N)
    if x0 * x0 < N:
        x0 = x0 + 1  # ceil(sqrt(N))

    # Iterate over successive values of x, bounded by s_bound
    for i in range(s_bound):
        # Current value of x in the iteration
        xi = x0 + i
        yi2 = xi * xi - N

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



N = 10000004400000259

print(f"N: {N}")
bounds = [i*1000000 for i in range(1, 100)]

times = []

for s in bounds:
    start = time.time()
    factors = Fermat_algorithm(N, s_bound=s)
    end = time.time()
    times.append(end - start)
    print("Factors:", factors)
    print("Execution Time:", end - start, "sec")

plt.plot(bounds, times)
plt.title("Execution time Fermat's Algorithm depending on s_bound")
plt.xlabel("s_bound")
plt.ylabel("Time")
plt.grid(True)
plt.savefig("fermats_runtime.png")
plt.show()
