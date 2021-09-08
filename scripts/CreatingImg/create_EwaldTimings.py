timings = [['SPME', 'PME', 'Ewald'],
            [0.3,    0.9,   3.8   ]]

FSSH_time = 0.37

import matplotlib.pyplot as plt



f, a = plt.subplots(1, 1, figsize=(16, 9))
a.bar(range(len(timings[0])), timings[1], color=(0.4, 0.3, 0.4))

a.set_xticks(range(len(timings[0])))
a.set_xticklabels(timings[0], fontsize=24)

a.axhline(FSSH_time, ls="--", color='k')

xlim = a.get_xlim()
a.annotate(f"Time for 1 FOB-SH step ({FSSH_time}s)", (xlim[0]+0.02, 0.37),
           va="bottom", ha="left", fontsize=24)
a.bar(range(len(timings[0])), timings[1],
      color=(0.4, 0.2, 0.4), zorder=3)
a.spines['left'].set_visible(False)
a.set_yticks([])


for i, t in enumerate(timings[1]):
    a.annotate(f"{t}s", (i, t-0.02), va="top", ha="center",
               color="white", fontsize=24, fontweight=500)

plt.savefig("../../img/ES/InitialTimings.png", dpi=250)

