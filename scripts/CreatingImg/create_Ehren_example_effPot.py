import numpy as np; import matplotlib.pyplot as plt

import plot_utils as ut

w = 3
x0 = 0

x = np.arange(-10, 10, 0.01)

# Gaussian Potential
pot1 = 2*(np.exp(-((x - x0)**2) / w**2) - 1)
pot1[x >= 0] *= 2 #warp gaussian a bit

pot2 = 3 - pot1.copy() # invert gaussian

pot1[x<0] *= 1.2 # Unsymmetrise gaussian/potentials

effPot = pot1.copy() # Create an effective potential for Ehrenfest
effPot[x > 0] *= 0.5



f, a = plt.subplots(figsize=(10, 9))

a.plot(x, pot1, color=ut.RED, lw=5)
a.plot(x, pot2, color=ut.BLUE, lw=5)
a.plot(x, effPot, 'k--', lw=4)

# Plot the atom and it's path
mask = (x < 7.4)
a.plot(x[mask], (effPot+0.17)[mask], '--', lw=2, color=ut.GREY)
arrx, arry = ut.create_arrow((7.4, -1.82544444444), 0.2, 20)
a.plot(arrx, arry, '-', lw=2, color=ut.GREY)
a.plot([-10], [-2.2], 'ko', ms=14)

a.annotate("Effective\nPotential", (7.5, -2), fontsize=ut.ANNOTATE_FONTSIZE,
           va="center")
a.annotate("PES 1", (7.5, -3.9), fontsize=ut.ANNOTATE_FONTSIZE, color=ut.RED)
a.annotate("PES 2", (7.5, 7.1), fontsize=ut.ANNOTATE_FONTSIZE, color=ut.BLUE)

a.grid(False)
a.spines['bottom'].set_visible(True)
a.set_xlabel("Reaction Coordinate", fontsize=22)
a.spines['top'].set_visible(False)
a.spines['right'].set_visible(False)
a.spines['left'].set_visible(True)
a.set_ylabel("Energy", fontsize=22)
a.set_xticks([])
a.set_yticks([])

#plt.show()

plt.savefig("../../img/Eh_hop.png", dpi=220)
