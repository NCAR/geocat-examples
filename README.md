![Build documentation pages](https://github.com/NCAR/GeoCAT-examples/workflows/Build%20documentation%20pages/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/geocat-examples/badge/?version=latest)](https://geocat-examples.readthedocs.io/en/latest/?badge=latest)


# GeoCAT-examples

GeoCAT-examples repo contains visualization examples that demonstrate how to use GeoCAT’s computational functions 
or how to plot data with packages in the Python ecosystem (primarily, Matplotlib and Cartopy).

Check out our [GeoCAT-Examples Gallery](https://geocat-examples.readthedocs.io/en/latest/) to see the example plots 
and to access Python code files as well as auto-generated Jupyter notebooks of this repo!

Several visualizations in this repository could be compared to NCL scripts from the 
[NCL Application Examples website](https://ncl.ucar.edu/Applications/).

A primary objective of this project is to identify any NCL plotting functionality that is missing from 
the popular Matplotlib + Cartopy toolchain, so each contributed script, if originating from NCL, should 
contain a best-effort attempt at reproducing an NCL graphic as closely as possible without using NCL or PyNGL. 
In the future, PyNGL examples may be included in this repository as well, but the current goal is to see what 
*can't* be done with Matplotlib and Cartopy.

That said, if you identify any NCL functionality in particular that does not seem to exist in 
Matplotlib/Cartopy, please create an issue on this repository's GitHub page with a link to the original 
NCL example page and list any NCL functions whose functionality is missing from Python.

As a secondary objective, this repository may also contain extended examples of the GeoCAT computational 
functions ([GeoCAT-comp](https://github.com/NCAR/geocat-comp)), which may be too long/complex to be included 
in the function's doc string and/or requires visualization for improved demonstration.


# Documentation

[GeoCAT Homepage](https://geocat.ucar.edu/)

[GeoCAT Contributor's Guide](https://geocat.ucar.edu/pages/contributing.html)

[GeoCAT-Examples Gallery](https://geocat-examples.readthedocs.io)

[NCL Application Examples](https://ncl.ucar.edu/Applications/)


# Installation instructions

Please see our documentation for [installation instructions](https://github.com/NCAR/geocat-examples/INSTALLATION.md). 
