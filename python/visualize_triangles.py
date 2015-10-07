# visualize_triangles.py
# This file is part of the Ptolemy Layer for Google Earth project.
# It helps us develop our intuition about the path we should be heading
# with model selection by allowing us to visualize how the triangles
# generated by the Delaunay triangulation actually move around as we
# go from Ptolemy coordinates to what we think are known coordinates.

import os
import sys
import math
import logging

import simplekml
import numpy as np
import pandas as pd
from geopy.distance import vincenty
from scipy.spatial import Delaunay

import sgdb
import geocode
import common

def write_triangle(kml, name, colors, points):
    for i in range(3):
        common.write_line(kml, points[i], points[(i+1) % 3], colors[i])

def write_triangle_visualization_kml(tri, known, unknown):
    """Compute unknown modern coordinates from known ones using the
    given triangulation."""
    colors = ['red', 'yellow', 'green']
    with open('../Data/visualize_triangles.kml', 'wb') as kml:
        kml.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        kml.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        kml.write('<Document>\n')
        common.write_styles(kml)
        for simp in tri.simplices:
            print simp
            tri_name = 'Triangle_%s' % '_'.join(str(x) for x in simp)
            kml.write('  <Folder id="%s">\n' % (tri_name, ))
            kml.write('      <name>%s</name>\n' % (tri_name, ))
            write_triangle(kml, tri_name, colors, [(known.ix[x].ptol_lat, known.ix[x].ptol_lon) for x in simp])
            write_triangle(kml, tri_name, colors, [(known.ix[x].modern_lat, known.ix[x].modern_lon) for x in simp])
            kml.write('  </Folder>\n')
        kml.write('</Document>\n')
        kml.write('</kml>\n')

if __name__ == '__main__':
    places = common.read_places()
    known, unknown = common.split_places(places)
    points = known.loc[:, ['ptol_lat','ptol_lon']]
    tri = Delaunay(points, furthest_site=False)
    write_triangle_visualization_kml(tri, known, unknown)