GeoCAT-examples Documentation
=============================

This gallery contains visualization examples from many plotting categories
of geosciences data.

Specifically, visualizations in this repository are intended to demonstrate Python ways of generating figures akin to the [NCL Application Examples website](https://ncl.ucar.edu/Applications/).

A primary objective of this project is to identify any NCL plotting functionality that is missing from
the popular Matplotlib + Cartopy toolchain, so each contributed script, if originating from NCL, should
contain a best-effort attempt at reproducing an NCL graphic as closely as possible without using NCL or PyNGL.
Read more about [NCAR's pivot-to-python](https://www.ncl.ucar.edu/Document/Pivot_to_Python/).

For visualization, mainly `matplotlib` and `cartopy` are used. In addition,
`geocat-datafiles <https://github.com/NCAR/geocat-datafiles>`_ is used as a
dataset storage and `geocat-viz <https://github.com/NCAR/geocat-viz>`_ is used for
a higher level implementation for low level `matplotlib` functionalities.
`Xarray` and `numpy` are used for data processing.

Gallery cards link to full image and source code, with download of Python script
enabled.

.. toctree::
   :maxdepth: 2
   :caption: Gallery
   :hidden:

   ./gallery/index

.. toctree::
   :caption: Usage
   :hidden:

   ./install
   ./citation

.. toctree::
   :caption: Contributing
   :hidden:

   ./contrib

.. toctree::
   :caption: Support
   :hidden:

   GitHub Issues <https://github.com/NCAR/geocat-examples/issues>
   Suggestion Box <https://forms.gle/6DTo3ELLri4DAGfG8>
