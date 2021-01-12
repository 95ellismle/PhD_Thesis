import numpy as np; import matplotlib.pyplot as plt

import plot_utils as ut

#Gaussian params
w = 3
x0 = 0
# Param for path
xshift = 0.35

x = np.arange(-10, 10, 0.01)

# Gaussian Potential
pot1 = 2*(np.exp(-((x - x0)**2) / w**2) - 1)
pot1[x >= 0] *= 2 #warp gaussian a bit

pot2 = 3 - pot1.copy() # invert gaussian

pot1[x<0] *= 1.2 # Unsymmetrise gaussian/potentials

# Create effective potential
mask = x < 0
maskLast = (x < 3.5) & (x >= xshift)
effX1 = list(x[mask])
effX2 = [0, 0]
effX3 = list(x[maskLast])
effX4 = effX3[::-1]
effX5 = effX1.copy()[::-1]
effX = np.array(effX1 + effX2 + effX3)
effPot1 =  list(pot1[mask])
effPot2 = [np.max(pot1), np.min(pot2)]
effPot3 = list(pot2[maskLast])
effPot4 = effPot3[::-1]
effPot5 = list(pot2[mask][::-1])
effPot = np.array(effPot1 + effPot2 + effPot3)





f, a = plt.subplots(figsize=(10, 9))

a.plot(x, pot1, color=ut.RED, lw=5)
a.plot(x, pot2, color=ut.BLUE, lw=5)
a.plot(effX, effPot, 'k--', lw=4)
a.plot(effX5, effPot5, 'k--', lw=4)


# Plot the atom and it's path (with arrows)
#Path
pathX = [i -0.1 for i in effX1] + \
        [xshift]*2 +              \
        list(x[maskLast]) + \
        list(x[maskLast][::-1])
pathY = list(np.array(effPot1)+0.2) + \
        [i+0.2 for i in effPot2] + \
        list(pot2[maskLast]+0.3) + \
        [val - 0.3*(i/(len(pot2[maskLast])+1)) for i, val in enumerate(list(pot2[maskLast]+1)[::-1], 1)]
lastX, lastY = pathX[-1], pathY[-1]
mask = (effX5 < lastX)
pathX += list(np.array(effX5)[mask])
finalY = list(np.array(effPot5)[mask] + 0.7)
finalY = [val - 0.09*((i/len(finalY)))**0.3 for i, val in enumerate(finalY)]
pathY += finalY


a.plot(pathX, pathY, '--', lw=2, color=ut.GREY)
#Arrow1
arrx, arry = ut.create_arrow((-0.1, 0.1973), 0.3, 20)
arrx, arry = ut.rot_points_2D((arrx, arry), 5, (-0.1, 0.1973))
a.plot(arrx, arry, '-', lw=2, color=ut.GREY)
#Arrow2
arrx, arry = ut.create_arrow((xshift, 2), 0.3, 30)
arrx, arry = ut.rot_points_2D((arrx, arry), 90, (xshift, 2))
a.plot(arrx, arry, '-', lw=2, color=ut.GREY)
#Arrow3
arrx, arry = ut.create_arrow((2.2321, 5), 0.3, 30)
arrx, arry = ut.rot_points_2D((arrx, arry), 50, (arrx[1], arry[1]))
a.plot(arrx, arry, '-', lw=2, color=ut.GREY)
#Arrow4
arrx, arry = ut.create_arrow((2.4, 5.78545), 0.3, 30)
arrx, arry = ut.rot_points_2D((arrx, arry), 232, (arrx[1], arry[1]))
a.plot(arrx, arry, '-', lw=2, color=ut.GREY)
#Arrow5
arrx, arry = ut.create_arrow((-5, 5.51827), 0.3, 30)
arrx, arry = ut.rot_points_2D((arrx, arry), 162, (arrx[1], arry[1]))
a.plot(arrx, arry, '-', lw=2, color=ut.GREY)


a.plot([-10], [-2.2], 'ko', ms=14)

a.annotate("Effective\nPotential", (-9.9, 4.9), fontsize=ut.ANNOTATE_FONTSIZE,
           va="top", color='k')
a.annotate("Atom's Path", (-9.9, 5.6), fontsize=ut.ANNOTATE_FONTSIZE,
           va="bottom", color=ut.GREY)
a.annotate("PES 1", (7.5, -3.9), fontsize=ut.ANNOTATE_FONTSIZE,
           color=ut.RED)
a.annotate("PES 2", (7.5, 7.1), fontsize=ut.ANNOTATE_FONTSIZE,
           color=ut.BLUE)

#a.grid(True)
a.spines['bottom'].set_visible(True)
a.set_xlabel("Reaction Coordinate", fontsize=22)
a.spines['top'].set_visible(False)
a.spines['right'].set_visible(False)
a.spines['left'].set_visible(True)
a.set_ylabel("Energy", fontsize=22)
a.set_xticks([])
a.set_yticks([])


plt.savefig("../../img/Sh_hop.png", dpi=220)
