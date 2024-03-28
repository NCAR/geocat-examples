| CI | [![GitHub Workflow Status][github-ci-badge]][github-ci-link] [![GitHub Workflow Status][github-upstream-ci-badge]][github-upstream-ci-link] |
| :----------- | :----------------------------------------------------------: |
| **Docs**     |       [![Documentation Status][rtd-badge]][rtd-link]         |
| **License**  |           [![License][license-badge]][repo-link]             |
| **Citing**   |               [![DOI][doi-badge]][doi-link]                  |

# GeoCAT-examples

GeoCAT-examples repo contains visualization examples that demonstrate how to how to plot data with packages in the Python ecosystem (primarily, Matplotlib and Cartopy).

Specifically, visualizations in this repository are intended to demonstrate Python ways of generating figures akin to the [NCL Application Examples website](https://ncl.ucar.edu/Applications/).

A primary objective of this project is to identify any NCL plotting functionality that is missing from
the popular Matplotlib + Cartopy toolchain, so each contributed script, if originating from NCL, should
contain a best-effort attempt at reproducing an NCL graphic as closely as possible without using NCL or PyNGL.
In the future, PyNGL examples may be included in this repository as well, but the current goal is to see what
*can't* be done with Matplotlib and Cartopy.

That said, if you identify any NCL functionality in particular that does not seem to exist in
Matplotlib/Cartopy, please create an issue on this repository's GitHub page with a link to the original
NCL example page and list any NCL functions whose functionality is missing from Python.


# Documentation

[GeoCAT Homepage](https://geocat.ucar.edu/)

[GeoCAT Contributor's Guide](https://geocat-examples.readthedocs.io/en/latest/contrib.html)

[GeoCAT-Examples Gallery](https://geocat-examples.readthedocs.io)

[NCL Application Examples](https://ncl.ucar.edu/Applications/)


# Installation instructions

Please see our documentation for [installation instructions](https://geocat-examples.readthedocs.io/en/latest/install.html).

# Citing GeoCAT-examples

If you use this software, please cite it as described at the [GeoCAT-examples - Citation](
https://geocat-examples.readthedocs.io/en/latest/citation.html) page.




[github-ci-badge]: https://img.shields.io/github/actions/workflow/status/NCAR/geocat-examples/ci.yml?label=CI&style=for-the-badge
[github-ci-link]: https://github.com/NCAR/geocat-examples/actions/workflows/ci.yml
[github-upstream-ci-badge]: https://img.shields.io/github/actions/workflow/status/NCAR/geocat-examples/upstream-dev-ci.yml?&label=Upstream%20CI&style=for-the-badge
[github-upstream-ci-link]: https://github.com/NCAR/geocat-examples/actions/workflows/upstream-dev-ci.yml
[rtd-badge]: https://img.shields.io/readthedocs/geocat-examples/latest.svg?style=for-the-badge
[rtd-link]: https://geocat-examples.readthedocs.io/en/latest/?badge=latest
[license-badge]: https://img.shields.io/github/license/NCAR/geocat-examples?style=for-the-badge
[doi-badge]: https://zenodo.org/badge/DOI/10.5281/zenodo.6678258.svg
[doi-link]: https://doi.org/10.5281/zenodo.6678258
[comment]: <> ([doi-badge]: https://img.shields.io/badge/DOI-10.5065%2Fa8pp--4358-brightgreen?style=for-the-badge)
[comment]: <> ([doi-link]: https://doi.org/10.5065/a8pp-4358)
[repo-link]: https://github.com/NCAR/geocat-examples
