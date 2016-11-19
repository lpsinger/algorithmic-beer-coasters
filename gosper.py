#!/usr/bin/env python
import numpy as np
from matplotlib import pyplot as plt

# Evaluate N iterations of the Lindenmayer sytem for the Gosper curve.
N = 2
sequence = 'A'
rules = {'A': 'A-B--B+A++AA+B-', 'B': '+A-BB--B-A++A+B'}
for _ in range(N):
    sequence = ''.join(rules.get(symbol, symbol) for symbol in sequence)

# Translate to vertices of a path.
nturns = 0
points = [np.zeros(2)]
for symbol in sequence:
    if symbol == '+':
        nturns += 1
    elif symbol == '-':
        nturns -= 1
    else:
        heading = nturns * np.pi / 3
        points.append(points[-1] + [np.cos(heading), np.sin(heading)])
points = np.asarray(points)

# Plot with Matplotlib.
fig = plt.figure(figsize=(4, 4))
ax = plt.axes(aspect='equal', frameon=False)
ax.axis('off')
ax.plot(*points.T)
fig.savefig('gosper.pdf')
