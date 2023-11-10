Installation
============

GeoCAT-examples is a collection of standalone visualization examples (not distributed
as a package on PyPI or conda-forge).

The easiest way to run multiple GeoCAT-examples scripts is to clone the GeoCAT-examples
repository. Then configure a `Conda <http://conda.pydata.org/docs/>`_ environment to run them in
as described below in `Creating a Conda environment`_.

To run individual GeoCAT-examples, you can also download the examples as scripts or Jupyter
notebooks by clicking the download buttons at the bottom of each example in the gallery. To set up
an environment in which to run the examples either ensure you have the packages mentioned
in the import packages section at the top of the script installed or install the full GeoCAT-examples
environment as described in `Creating a Conda environment`_.

Creating a Conda environment
----------------------------

This repository provides a `Conda environment file <https://github.com/NCAR/geocat-examples/blob/main/conda_environment.yml>`_
that can be used to create an evironment to run the examples included in this gallery. 

To create a Conda environment using the file provided by this repo, from the root directory of
the cloned geocat-examples repository (or the directory containing the ``conda_environment.yml``
file you downloaded), run the following commands::

    conda env create -f conda_environment.yml -n geocat-examples
    conda activate geocat-examples

Note that the Conda package manager automatically installs all of the `required`
dependencies of GeoCAT-examples listed under ``conda_environment.yml`` file (such as ``geocat-comp``,
``geocat-datafiles``, ``cartopy``, ``matplotlib``, ``netcdf4``, etc.). There is no need to
explicitly install these packages.

If you are interested in learning more about how Conda environments work, please visit
the `managing environments <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`_
page of the Conda documentation.
