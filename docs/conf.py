# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

# -- Project information -----------------------------------------------------

project = 'GeoCAT-examples'

import datetime

current_year = datetime.datetime.now().year
copyright = u'{}, University Corporation for Atmospheric Research'.format(
    current_year)
author = u'GeoCAT'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx_gallery.gen_gallery',
    'nbsphinx',
    'sphinx_gallery.load_style',
]

# Define what extensions will parse which kind of source file
source_suffix = {
    '.md': 'sphinx_gallery',
    '.rst': 'restructuredtext',
}

image_scrapers = ('matplotlib',)

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**/README.rst']

# Set plotly renderer to capture _repr_html_ for sphinx-gallery
try:
    import plotly.io as pio
    pio.renderers.default = 'sphinx_gallery'
except ImportError:
    pass

# -- suppress warnings -------------------------------------------------------
import warnings

# filter Matplotlib 'agg' warnings
warnings.filterwarnings("ignore",
                        category=UserWarning,
                        message='Matplotlib is currently using agg, which is a'
                        ' non-GUI backend, so cannot show the figure.')

# filter seaborn warnings
warnings.filterwarnings("ignore",
                        category=UserWarning,
                        message='As seaborn no longer sets a default style on'
                        ' import, the seaborn.apionly module is'
                        ' deprecated. It will be removed in a future'
                        ' version.')

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
import sphinx_rtd_theme

html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ['_static']
html_logo = '_static/images/nsf.png'
html_style = None


# Allow for changes to be made to the css in the theme_overrides file
def setup(app):
    app.add_css_file('theme_overrides.css')


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Specify master_doc (see https://github.com/readthedocs/readthedocs.org/issues/2569#issuecomment-485117471)
master_doc = 'index'

# Configure sphinx-gallery plugin
from sphinx_gallery.sorting import ExampleTitleSortKey

sphinx_gallery_conf = {
    'examples_dirs': ['../Plots', '../GeoCAT-comp-examples'
                     ],  # path to your example scripts
    'filename_pattern': '^((?!sgskip).)*$',
    'gallery_dirs': ['gallery', 'gallery-geocat-comp'
                    ],  # path to where to save gallery generated output
    'within_subsection_order': ExampleTitleSortKey,
    'matplotlib_animations': True,
}

html_theme_options = {
    'navigation_depth': 2,
}

import logging

# the following lines suppress INFO messages when files are downloaded using geocat.datafiles
import geocat.datafiles
import pooch

logger = pooch.get_logger()
logger.setLevel(logging.WARNING)
geocat.datafiles.get("registry.txt")

nbsphinx_prolog = """
Download notebook (Right click and save):
https://github.com/NCAR/GeoCAT-examples/raw/main/docs/{{ env.doc2path(env.docname, base=None) }}

----
"""
