# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os

import logging

# the following lines suppress INFO messages when files are downloaded using geocat.datafiles
import geocat.datafiles
import pooch

logger = pooch.get_logger()
logger.setLevel(logging.WARNING)
geocat.datafiles.get("registry.txt")

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

# -- Project information -----------------------------------------------------

project = u'GeoCAT-examples'

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
    "sphinx_design",
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
html_theme = 'sphinx_book_theme'
html_title = ""
html_static_path = ['_static']
html_favicon = '_static/images/GeoCAT_square.svg'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = ["theme_overrides.css"]

html_theme_options = {
    "repository_url": "https://github.com/NCAR/geocat-examples",
    "repository_branch": "main",
    "path_to_docs": "docs",
    "use_edit_page_button": True,
    "use_repository_button": True,
    "use_issues_button": True,
    "home_page_in_toc": False,
    "navbar_footer_text": "",
    "logo": {
        "image_light": '_static/images/NSF_NCAR_light.svg',
        "image_dark": '_static/images/NSF_NCAR_dark.svg',
    }
    "extra_footer": "<em>This material is based upon work supported by the NSF National Center for Atmospheric Research, a major facility sponsored by the U.S. National Science Foundation and managed by the University Corporation for Atmospheric Research. Any opinions, findings and conclusions or recommendations expressed in this material do not necessarily reflect the views of the U.S. National Science Foundation.</em>",
}

# Specify master_doc (see https://github.com/readthedocs/readthedocs.org/issues/2569#issuecomment-485117471)
master_doc = 'index'

# Configure sphinx-gallery plugin
from sphinx_gallery.sorting import ExampleTitleSortKey

sphinx_gallery_conf = {
    'examples_dirs': ['../Gallery'],  # path to your example scripts
    'filename_pattern': '^((?!sgskip).)*$',
    'gallery_dirs': ['gallery',
                    ],  # path to where to save gallery generated output
    'within_subsection_order': ExampleTitleSortKey,
    'matplotlib_animations': True,
}

# Configure nbsphinx
nbsphinx_prolog = """
Download notebook (Right click and save):
https://github.com/NCAR/GeoCAT-examples/raw/main/docs/{{ env.doc2path(env.docname, base=None) }}

----
"""
