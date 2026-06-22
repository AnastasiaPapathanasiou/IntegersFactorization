import time
import random
import matplotlib.pyplot as plt
from fermats_method import fermat_algorithm


def plot_time_vs_factor_distance(p, distances):
    times = []

    print("\nTesting dependence on |p - q|\n")

    for d in distances:
        q = p + d
        n = p * q

        start = time.time()
        factors = fermat_algorithm(n, s_bound=d + 10)  # small buffer
        end = time.time()

        times.append(end - start)
        print("Factors:", factors)
        print("Time:", end - start, "sec\n")

    # Normal scale
    plt.figure()
    plt.plot(distances, times)
    plt.xlabel("|p - q|")
    plt.ylabel("Execution time (seconds)")
    plt.title("Fermat method: Time vs |p − q|")
    plt.grid(True)
    plt.savefig("fermat_time_vs_distance.png")
    plt.close()

    # Log scale
    plt.figure()
    plt.plot(distances, times)
    plt.yscale("log")
    plt.xlabel("|p - q|")
    plt.ylabel("Execution time (log scale)")
    plt.title("Fermat method: Time vs |p − q| (log scale)")
    plt.grid(True, which="both")
    plt.savefig("fermat_time_vs_distance_log.png")
    plt.close()


# Example prime (moderate size)
p = 10000019
distances = [10, 50, 100, 500, 1000, 5000, 10000, 50000]

plot_time_vs_factor_distance(p, distances)
