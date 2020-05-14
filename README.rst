OSM Missing Addresses Finder
============================

The OSM Missing Addresses Finder takes the OSM ID of an area, and an Excel list of addresses in a certain area (e.g. from an authority).
It queries Overpass for the addresses currently entered in OpenStreetMap, and computes the difference.
The missing addresses are written into an .osm file, which can be loaded in JOSM.
