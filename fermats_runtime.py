import time
import os
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from fermats_method import fermat_algorithm

# Setup files
os.makedirs("results", exist_ok=True)
os.makedirs("plots", exist_ok=True)

ns = [50651849296460476429, 126204041959255639109, 15241498157936126579312244973, 1524157875735101476256211, 15241578753238836750190515, 152415787532388367501905489477, 15241578753238836750190518424398338]
for n in ns:
    print(f"n: {n}")
    bounds = [i*100000000 for i in range(1, 100000)]

# CSV
csv_path = "results/fermat_results.csv"

with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["n", "s_bound", "time_sec", "factors"])

    # Batch run
    for n in ns:
        print(f"\nRunning for n = {n}")
        times = []

        for s in bounds:
            start = time.time()
            factors = fermat_algorithm(n, s)
            end = time.time()

            exec_time = end - start
            times.append(exec_time)

            print(f"s={s} | time={exec_time:.6f} sec | factors={factors}")
            writer.writerow([N, s, exec_time, factors])

# Διάγραμμα (normal)
plt.figure()
plt.plot(bounds, times, marker="o")
plt.title(f"Fermat Execution Time (N={N})")
plt.xlabel("s_bound")
plt.ylabel("Time (sec)")
plt.grid(True)
plt.savefig(f"plots/fermat_N_{N}.png")
plt.close()

# Διάγραμμα (log scale)
plt.figure()
plt.plot(bounds, times, marker="o")
plt.yscale("log")
plt.title(f"Fermat Execution Time – Log Scale (N={N})")
plt.xlabel("s_bound")
plt.ylabel("Time (sec, log)")
plt.grid(True, which="both")
plt.savefig(f"plots/fermat_N_{N}_log.png")
plt.close()

print("\n Finished")