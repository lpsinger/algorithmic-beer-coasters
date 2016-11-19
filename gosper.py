#!/usr/bin/env python
from math import pi, cos, sin

# Evaluate N iterations of the Lindenmayer sytem for the Gosper curve.
N = 2
sequence = 'A'
rules = {'A': 'A-B--B+A++AA+B-', 'B': '+A-BB--B-A++A+B'}
for _ in range(N):
    sequence = ''.join(rules.get(symbol, symbol) for symbol in sequence)

# Translate to vertices of a path.
nturns = 0
d = 'M0,0'
for symbol in sequence:
    if symbol == '+':
        nturns += 1
    elif symbol == '-':
        nturns -= 1
    else:
        heading = nturns * pi / 3
        d += ' l{:g},{:g}'.format(cos(heading), sin(heading))

svg = """\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="-10 -10 20 20">
<path d="{}" style="stroke: black; fill: none; stroke-width: 0.01pt"/>
</svg>
""".format(d)

with open('gosper.svg', 'w') as f:
    f.write(svg)
