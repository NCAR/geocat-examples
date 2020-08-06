# Installation

This installation guide includes only the GeoCAT-examples installation instructions. 
Please refer to [GeoCAT Contributor's Guide](https://geocat.ucar.edu/pages/contributing.html) for installation of 
the whole GeoCAT project.
  

## Installing GeoCAT-examples

GeoCAT-examples is not distributed as a conda package; thus, there is no conda installation for it.

The easiest way to access GeoCAT-examples is cloning the repo and then using a 
[Conda](http://conda.pydata.org/docs/) environment, building file of which is provided in this repo, as follows:

### How to create a GeoCAT-examples Conda environment

From the root directory of the cloned geocat-examples repository, run the following commands:
```
    conda env create -f conda_environment.yml -n geocat-examples
    conda activate geocat-examples
```

 contains the dependencies for the required software packages, 
such as ; therefore, there is no need for 
explicitly installing those packages.

Also, note that the Conda package manager automatically installs all `required`
dependencies listed under `conda_environment.yml` file, meaning it is not necessary 
to explicitly install Python, Matplotlib, Cartopy, Scikit-learn, Jupyter, etc. when 
creating an environment.

If you are interested in learning more about how Conda environments work, please visit 
the [managing environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) 
page of the Conda documentation.

