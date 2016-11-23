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

# Create Gosper curve geometry.
gosper = geometry.LineString(points)

# Create exterior of coaster.
exterior = gosper.envelope.buffer(1).exterior

# Determine bounding box for artwork.
minx, miny, maxx, maxy = exterior.bounds
width = maxx - minx; height = maxy - miny

# Start SVG document.
pad = 1
print('<svg xmlns="http://www.w3.org/2000/svg"')
print('viewBox="{} {} {} {}" width="4in" height="4in">'.format(
      minx - pad, miny - pad, width + 2 * pad, height + 2 * pad))
svgargs = dict(scale_factor=0.05, stroke_color='red')

# Write Gosper curve and exterior.
print(gosper.svg(**svgargs))

# Write exterior.
print(exterior.svg(**svgargs))

# Write lines connecting Gosper curve to exterior.
endpoint = gosper.coords[0]
print(geometry.LineString([endpoint, [minx, endpoint[1]]]).svg(**svgargs))
endpoint = gosper.coords[-1]
print(geometry.LineString([endpoint, [maxx, endpoint[1]]]).svg(**svgargs))

# End SVG document.
print('</svg>')
