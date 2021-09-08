import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

num_words = 20

df = pd.read_csv('top_words.csv', names=('word','size'), skiprows=[0])


f, a = plt.subplots()


def get_xy_raw(i):
    """will get the xy coords of each word"""
    r = (2 * i) ** (0.3  ** (1/(0.1*i+1)))
    theta = i * 2 * np.pi / 7
    return r * np.cos(theta), r * np.sin(theta)


maxX, maxY = -float("inf"), -float("inf")
minX, minY =  float("inf"),  float("inf")
for i in range(num_words):
    row = df.iloc[i]
    word, size = row['word'], row['size']
    x, y = get_xy_raw(i)

    if x < minX: minX = x
    if x > maxX: maxX = x
    if y < minY: minY = y
    if y > maxY: maxY = y

    a.annotate(word, (x, y), fontsize=size*36)


minX, maxX = np.ceil(minX), np.ceil(maxX)
minY, maxY = np.ceil(minY), np.ceil(maxY)


###
# Prettify
##
#for i in ('top', 'bottom', 'left', 'right'):
#    a.spines[i].set_visible(False)
#a.set_xticks([])
#a.set_yticks([])
a.set_xlim([minX - 1, maxX + 1])
a.set_ylim([minY, maxY])

plt.show()
