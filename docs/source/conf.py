# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

# -- Project information -----------------------------------------------------

project = "libzapi"
copyright = "2025, Leandro Meili"
author = "Leandro Meili"
release = "0.9.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = []

autodoc_member_order = "bysource"

# -- Options for HTML output -------------------------------------------------

html_theme = "furo"
html_theme_options = {
    "source_repository": "https://github.com/BCR-CX/libzapi",
    "source_branch": "main",
    "source_directory": "docs/source/",
}
html_static_path = ["_static"]
