#!/usr/bin/env bash
# adapted from https://github.com/pydata/xarray/blob/main/ci/install-upstream-wheels.sh

# forcibly remove packages to avoid artifacts
conda remove -y --force \
    metpy \
    numpy \
    pandas \
    scipy \
    xarray \
    matplotlib \
    geocat-viz \
    geocat-comp

# conda list
conda list

# if available install from nightly wheels
python -m pip install \
    -i https://pypi.anaconda.org/scipy-wheels-nightly/simple \
    --no-deps \
    --pre \
    --upgrade \
    numpy \
    pandas \
    scipy \
    xarray \
    matplotlib

# install rest from source
python -m pip install \
    git+https://github.com/Unidata/MetPy.git \
    git+https://github.com/NCAR/geocat-comp \
    git+https://github.com/NCAR/geocat-viz
