Installation
============

Create a GeoCAT-examples Conda environment
------------------------------------------
In order to run any of the example scripts on this website, you will need to
install the necessary Python packages. The simplest way to install these
packages is by using `conda <https://docs.conda.io/projects/conda/en/latest/>`_.
We generally recommend using Miniconda rather than Anaconda because it only
includes the bare minimum amount of software needed to create new conda
environments, while Anaconda includes many Python packages by default (which may
not be perfectly compatible with the builds of GeoCAT software we provide).

Once you have conda installed, you can create a new ``geocat-examples`` conda
environment with either of the following methods:

* Download the file :download:`conda_environment.yml <../conda_environment.yml>` and then run::

    conda env create -f conda_environment.yml -n geocat-examples

or alternatively:

* Run the command::

   conda create -c conda-forge -c ncar -n geocat-examples python=3 geocat-comp geocat-datafiles geocat-viz=2020.2.18.1 netcdf4 matplotlib cartopy jupyter

In either case, you can "activate" your newly created environment by running::

    conda activate geocat-examples
