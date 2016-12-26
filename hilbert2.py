#!/usr/bin/env python
"""

              a l g o r i t h m i c   c o a s t e r   n o .   3
               ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
              Two procedurally generated fractal beer coasters.

                               by Leo P. Singer

                        This work is licensed under a
      Creative Commons Attribution-ShareAlike 4.0 International License
              (http://creativecommons.org/licenses/by-sa/4.0/).

"""
import numpy as np
from shapely import geometry

# Evaluate Lindenmayer system to generate the Hilbert curve.
sequence = 'X'
rules = {'X': 'XFYFX+F+YFXFY-F-XFYFX', 'Y': 'YFXFY-F-XFYFX+F+YFXFY'}
for _ in range(3):
    sequence = ''.join(rules.get(symbol, symbol) for symbol in sequence)

# Translate to vertices of a path.
nturns = 0
points = [np.zeros(2)]
for symbol in sequence:
    if symbol == '+':
        nturns += 1
    elif symbol == '-':
        nturns -= 1
    elif symbol == 'F':
        heading = nturns * np.pi / 2
        points.append(points[-1] + [np.cos(heading), np.sin(heading)])

# Create curve geometry.
curve = geometry.LineString(points)

# Create exterior of coaster.
exterior = curve.envelope.buffer(1).exterior

# Determine bounding box for artwork.
minx, miny, maxx, maxy = exterior.bounds
width = maxx - minx; height = maxy - miny

# Connect curve to exterior.
points[:0] = [[minx, points[0][1]]]
points[-1:] = [[maxx, points[-1][1]]]
proj = geometry.Point(points[-1])
i = np.argmin([pt.distance(proj) for pt in geometry.asMultiPoint(exterior)])
points += exterior.coords[i:]
points += exterior.coords[:i + 1]

# Write SVG document.
pad = 1
print('<svg xmlns="http://www.w3.org/2000/svg"')
print('viewBox="{} {} {} {}" width="4in" height="4in">'.format(
      minx - pad, miny - pad, width + 2 * pad, height + 2 * pad))
print(geometry.LineString(points).svg(scale_factor=0.05, stroke_color='red'))
print('</svg>')
