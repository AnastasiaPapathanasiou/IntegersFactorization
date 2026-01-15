import time
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

from fermats_method import fermat_algorithm

ns = [50651849296460476429, 126204041959255639109, 15241498157936126579312244973, 1524157875735101476256211, 15241578753238836750190515, 152415787532388367501905489477, 15241578753238836750190518424398338]
for n in ns:
    print(f"n: {n}")
    bounds = [i*10000000 for i in range(1, 10000)]

    times = []

    for s in bounds:
        start = time.time()
        factors = fermat_algorithm(n, s_bound=s)
        end = time.time()
        times.append(end - start)
        print("Factors:", factors)
        print("Execution Time:", end - start, "sec")

plt.plot(bounds, times)
plt.title("Execution time Fermat's Algorithm depending on s_bound")
plt.xlabel("s_bound")
plt.ylabel("Time")
plt.grid(True)
plt.savefig("fermat_runtime.png")
plt.show()