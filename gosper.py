#!/usr/bin/env python
"""

              a l g o r i t h m i c   c o a s t e r   n o .   1
               ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
              Two procedurally generated fractal beer coasters.

                               by Leo P. Singer

                        This work is licensed under a
      Creative Commons Attribution-ShareAlike 4.0 International License
              (http://creativecommons.org/licenses/by-sa/4.0/).

"""
import numpy as np
from shapely import geometry

# Evaluate Lindenmayer system to generate the Gosper curve.
sequence = 'A'
rules = {'A': 'A-B--B+A++AA+B-', 'B': '+A-BB--B-A++A+B'}
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
    else:
        heading = nturns * np.pi / 3
        points.append(points[-1] + [np.cos(heading), np.sin(heading)])

# Create curve geometry.
curve = geometry.LineString(points)

# Create exterior of coaster.
exterior = curve.envelope.buffer(1).exterior

# Connect curve to exterior.
for _ in range(2):
    proj = exterior.interpolate(exterior.project(geometry.Point(points[0])))
    points = points[::-1] + [proj]
i = np.argmin([pt.distance(proj) for pt in geometry.asMultiPoint(exterior)])
points += exterior.coords[i:]
points += exterior.coords[:i + 1]

# Determine bounding box for artwork.
minx, miny, maxx, maxy = exterior.bounds
pad = 1
minx -= pad; maxx += pad; miny -= pad; maxy += pad
width = maxx - minx; height = maxy - miny

# Write SVG document.
print('<svg xmlns="http://www.w3.org/2000/svg"')
print('viewBox="{} {} {} {}" width="4in" height="4in">'.format(
      minx, miny, width, height))
print(geometry.LineString(points).svg(scale_factor=0.05, stroke_color='red'))
print('</svg>')
