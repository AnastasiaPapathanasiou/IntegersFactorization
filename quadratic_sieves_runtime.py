import time, csv, os
import matplotlib.pyplot as plt

from quadratic_sieve import quadratic_sieve



ns = [20687446319452874887189133]
# b_values for running the algorithm
b_values = [10000] #, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 50000]
interval = 50000

os.makedirs("results_QS", exist_ok=True)
os.makedirs("plots_QS", exist_ok=True)

with open("results_QS/quadratic_sieve_results.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["n", "b", "factor", "time_sec"])

    for n in ns:
        execution_times = []
        for b in b_values:
            start_time = time.time()
            factor = quadratic_sieve(n, b, interval)
            end_time = time.time()
            execution_time = end_time - start_time
            execution_times.append(execution_time)
            writer.writerow([n, b, factor, execution_time])
            print(f"n={n}, b={b}, factor={factor}, time={execution_time:.2f} sec")

            if factor != 0:  # We stop for this n when we find the factors
                break

        # Normal plot
        plt.figure()
        plt.plot(b_values[:len(execution_times)], execution_times)
        plt.title("Execution time Quadratic Sieve depending on B-smooth bound")
        plt.xlabel("B-smooth bound (B)")
        plt.ylabel("Execution time")
        plt.grid(True)
        plt.savefig(f"plots/quadratic_sieve_n_{n}.png")
        plt.close()

        # Log scale plot
        plt.figure()
        plt.plot(b_values[:len(execution_times)], execution_times, marker="o")
        plt.yscale("log")
        plt.title(f"Execution time Quadratic Sieve (log scale) for n={n}")
        plt.xlabel("B-smooth bound (B)")
        plt.ylabel("Execution time (sec, log)")
        plt.grid(True, which="both")
        plt.savefig(f"plots/quadratic_sieve_n_{n}_log.png")
        plt.close()