# Installation

This installation guide includes only the GeoCAT-examples installation instructions.
Please refer to [GeoCAT Contributor's Guide](https://geocat.ucar.edu/pages/contributing.html) for installation of
the whole GeoCAT project.


## Building GeoCAT-examples

GeoCAT-examples is a collection of standalone visualization examples, and it is not distributed
as a conda package; thus, there is no installation for it (via conda or other package management systems).

The easiest way to access GeoCAT-examples scripts as a whole is by cloning the repo and then using a
[Conda](http://conda.pydata.org/docs/) environment.

### Creating a Conda environment

The GeoCAT-examples repository has two different types of implementation for visualization examples:

1. Python scripts (`.py`) under the "Gallery" and "GeoCAT-comp-examples" directories
2. Jupyter notebooks under the "docs/gallery-notebooks" directory

This repository provides a Conda environment file that can be used to create an evironment to build
both (1) and (2). However, each of Jupyter notebooks under (2) will require their own additional
dependencies that are written in the beginning of them and needs to be installed into the active
Conda environment. Furthermore, users with advanced Conda knowledge will see that the Conda environment
file provided in this repo contains much more dependencies than the base Conda environment reuqires (i.e.
essentially a Jupyter technology such as Jupyter Lab to execute notebooks) to build (2).

In order to create a Conda environment using the file provided by this repo, from the root directory of
the cloned geocat-examples directory, run the following commands:

```
    conda env create -f conda_environment.yml -n geocat-examples
    conda activate geocat-examples
```

Note that the Conda package manager automatically installs all the `required`
dependencies of GeoCAT-examples listed under `conda_environment.yml` file (such as `geocat-comp`,
`geocat-datafiles`, `cartopy`, `matplotlib`, `netcdf4`, etc.); therefore, there is no need for
explicitly installing those packages.

If you somewhat need to make use of other software packages with GeoCAT-examples or are interested in
running the Jupyter notebooks under (2) mentioned above, you may wish/need to install them into your
`geocat-examples` environment at anytime with a command as in the
following example (assuming your `geocat-examples` environment is already activated):

    conda install -c bokeh bokeh

or in the way that is suggested by each Jupyter notebook under (2).

If you are interested in learning more about how Conda environments work, please visit
the [managing environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
page of the Conda documentation.
