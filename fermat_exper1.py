import time
import math
import matplotlib.pyplot as plt
from fermats_method import fermat_algorithm


def plot_time_vs_bound(n, bounds):
    times = []
    print(f"\nTesting n = {n}\n")

    for s in bounds:
        print(f"Running with s_bound = {s}")
        start = time.time()
        factors = fermat_algorithm(n, s)
        end = time.time()

        times.append(end - start)

        print("Factors:", factors)
        print("Time:", end - start, "sec\n")

        # Stop once factors are found
        if factors is not None:
            break


    # Normal scale plot
    plt.figure()
    plt.plot(bounds[:len(times)], times)
    plt.xlabel("Iteration bound (s_bound)")
    plt.ylabel("Execution time (seconds)")
    plt.title("Fermat method: Time vs iteration bound")
    plt.grid(True)
    plt.savefig("fermat_time_vs_bound.png")
    plt.close()

    # Log scale plot
    plt.figure()
    plt.plot(bounds[:len(times)], times)
    plt.yscale("log")
    plt.xlabel("Iteration bound (s_bound)")
    plt.ylabel("Execution time (log scale)")
    plt.title("Fermat method: Time vs iteration bound (log scale)")
    plt.grid(True, which="both")
    plt.savefig("fermat_time_vs_bound_log.png")
    plt.close()


# Example
n = 15241578753238836750190515
bounds = [i * 50000 for i in range(1, 200)]

plot_time_vs_bound(n, bounds)
