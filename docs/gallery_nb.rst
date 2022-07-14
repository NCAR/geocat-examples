Notebook Gallery
================
.. Warning::
    This version of the gallery uses experimental features from
    `geocat-viz <https://github.com/NCAR/geocat-viz>`_. We advise against
    using this version of the gallery to learn how to make visualizations,
    as it will be minimally maintained for plotting accuracy. However, we
    still want to provide it as a sneak peak for the GeoCAT user community.
    To see the latest stable version of the gallery, click on the version
    at the bottom of the contents panel on the left and select ``latest``.

This gallery contains visualization examples that are solely implemented in the
Jupyter notebook format (i.e. no `.py` script). Most, if not all, of these
notebooks are interactive  (i.e. the rendered images can be panned, zoomed,
etc). However, these notebooks are currently pre-rendered only, i.e. the
gallery only shows static renderings of the notebooks (Notebooks won't actually
show any greater resolution when the user zooms a plot; the user can zoom in all
they like, but the data is never re-rendered). To fully experience
the power of interactive exploration within a notebook, it will need to be
downloaded and executed locally as described below.

If the reader would like to execute these notebooks in their local setup, they
will need to have a conda environment that includes a Jupyter technology of
preference (e.g. Jupyter Lab, etc.). For further details about how to create
such an environment, please refer to the `Installation document
<https://github.com/NCAR/GeoCAT-examples/blob/main/INSTALLATION.md>`_ of this repo.

In addition to the above environment, each notebook
example lists its own dependencies that should be installed as well.

.. nbgallery::
   ./gallery-notebooks/Datashader/MPAS_Datashader_Trimesh
