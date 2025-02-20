#!/usr/bin/env bash
# adapted from https://github.com/pydata/xarray/blob/main/ci/install-upstream-wheels.sh

# forcibly remove packages to avoid artifacts
conda remove -y --force \
    metpy \
    pandas \
    scipy \
    xarray \
    matplotlib \
    geocat-viz \
    geocat-comp \
    cartopy

# conda list
conda list

# if available install from nightly wheels
python -m pip install \
    --index-url https://pypi.anaconda.org/scientific-python-nightly-wheels/simple \
    --extra-index-url https://pypi.org/simple \
    --no-deps \
    --pre \
    --upgrade \
    pandas \
    scipy \
    xarray \
    matplotlib

# install rest from source
python -m pip install \
    git+https://github.com/Unidata/MetPy.git \
    git+https://github.com/NCAR/geocat-comp.git \
    git+https://github.com/NCAR/geocat-viz.git \
    git+https://github.com/SciTools/cartopy.git
