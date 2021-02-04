import numpy as np
import matplotlib.pyplot as plt


quench_times = [0, 1, 10, 100]
OOPl = [0.00, 0.04, 0.28, 0.73]
OOPs = [0.00, 0.01, 0.30, 0.47]
sConv = 0.5*(3*(np.cos((np.pi*54.3/180.)/2)**2) - 1)

plt.figure(figsize=(20,10))

lnl, = plt.plot(quench_times, OOPl, 'o--', lw=1,
                ms=15, label=r"Long Axis")
lns, = plt.plot(quench_times, OOPs, 'o--', lw=1,
                ms=15, label=r"Short Axis")

plt.axhline(1, color=lnl.get_color(), lw=2.5, ls=':')
plt.axhline(sConv, color=lns.get_color(), lw=2.5, ls=':')

plt.ylabel("Orientational Order Parameter", fontsize=20)
plt.xlabel("Quench Time [ns]", fontsize=20)

plt.xscale("log")

plt.annotate("Long Axis Crystal OOP", (1, 1), fontsize=18)
plt.annotate("Short Axis Crystal OOP", (1, sConv), fontsize=18)

plt.legend(fontsize=20)

plt.savefig("../../img/DifferentQuenchTimes/TimevsOOP.png", dpi=220)
plt.show()

