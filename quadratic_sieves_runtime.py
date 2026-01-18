import time
import matplotlib.pyplot as plt

from quadratic_sieve import quadratic_sieve

# b_values for running the algorithm
b_values = [100, 200, 300, 400, 500, 600, 700]
execution_times = []

n = 1000000000000000000420000000000000000117
interval = 5000

for b in b_values:
    start_time = time.time()
    quadratic_sieve(n, b, interval)
    end_time = time.time()

    execution_time = end_time - start_time
    execution_times.append(execution_time)
    print(f"B={b}, Execution Time: {execution_time} sec")

# graph
plt.plot(b_values, execution_times)
plt.title("Execution time Quadratic Sieve depending on B-smooth bound")
plt.xlabel("B-smooth bound (B)")
plt.ylabel("Execution time")
plt.grid(True)
plt.show()