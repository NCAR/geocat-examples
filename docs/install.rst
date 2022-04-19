Installation
============

GeoCAT-examples is a collection of standalone visualization examples, and it is not distributed
as a conda package; thus, there is no installation for it (via conda or other package management systems).
The easiest way to access GeoCAT-examples scripts as a whole is by cloning the repo and then using a
`Conda <http://conda.pydata.org/docs/>`_ environment.

For information about installing the entire GeoCAT project, see our
`Contributor's Guide <(https://geocat.ucar.edu/pages/contributing.html#3-creating-a-development-environment)>`_.

Creating a Conda environment
----------------------------

The GeoCAT-examples repository has two different types of implementation for visualization examples:

1.  Python scripts (:code:`.py`) under the "Gallery" and "GeoCAT-comp-examples" directories
2.  Jupyter notebooks under the "docs/gallery-notebooks" directory

This repository provides a Conda environment file that can be used to create an evironment to build
both (1) and (2). However, each of Jupyter notebooks under (2) will require their own additional
dependencies that are written in the beginning of them and needs to be installed into the active
Conda environment. Furthermore, users with advanced Conda knowledge will see that the Conda environment
file provided in this repo contains much more dependencies than the base Conda environment reuqires (i.e.
essentially a Jupyter technology such as Jupyter Lab to execute notebooks) to build (2).

In order to create a Conda environment using the file provided by this repo, from the root directory of
the cloned geocat-examples directory, run the following commands::

    conda env create -f conda_environment.yml -n geocat-examples
    conda activate geocat-examples

Note that the Conda package manager automatically installs all the `required`
dependencies of GeoCAT-examples listed under :code:`conda_environment.yml` file (such as :code:`geocat-comp`,
:code:`geocat-datafiles`, :code:`cartopy`, :code:`matplotlib`, :code:`netcdf4`, etc.); therefore, there is no need for
explicitly installing those packages.

If you need to make use of other software packages with GeoCAT-examples or are interested in
running the Jupyter notebooks under (2) mentioned above, you may need to install them into your
:code:`geocat-examples` environment at anytime with a command as in the
following example (assuming your :code:`geocat-examples` environment is already activated)::

    conda install -c bokeh bokeh

or in the way that is suggested by each Jupyter notebook under (2).


Updating the :code:`geocat-examples` environment
------------------------------------------------
It is important to keep your environment up to date so you get the latest bugfixes and changes.
This can be done as follows:

Make sure your Conda is up to date by running this command from the terminal::

    conda update conda

Activate the conda environment you want to update::

    conda activate geocat-examples

Update all packages in the environment::

    conda update --all

Note that this will update all packages to the most recent version that is compatible with the other packages in the
environment. You may notice with :code:`conda list` that not every package in your environment is the latest version.
This is generally okay.

If you are interested in learning more about how Conda environments work, please visit
the `managing environments <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`_
page of the Conda documentation.
