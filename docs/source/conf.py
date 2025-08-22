# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import inspect

import os
import sys
import ocf_tools

sys.path.insert(0, os.path.abspath('../../'))
sys.path.insert(0, os.path.abspath('../../ocf_tools'))
sys.path.insert(0, os.path.abspath('../../ocf_tools/test'))

# -- Project information -----------------------------------------------------

project = 'OCF_Tools'
copyright = '2025, Scott A. Socolofsky'
author = 'Scott A. Socolofsky'

# The full version, including alpha/beta/rc tags
version = ocf_tools.__version__.split("+")[0]
release = ocf_tools.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.intersphinx',
    'numpydoc',
    'sphinx_copybutton',
    'sphinx_design',
    'matplotlib.sphinxext.plot_directive',
    'myst_nb',
    'jupyterlite_sphinx',
]

autosummary_generate = True
autodoc_typehints = "none"

napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_use_param = False
napoleon_use_rtype = False
napoleon_preprocess_types = True
napoleon_type_aliases = {
    "tamoc": ":term:`tamoc`",
    "array": ":term:`array`",
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build']
pygments_style = 'sphinx'

# The suffix of source filenames.
#source_suffix = '.rst'
master_doc = 'index'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'pydata_sphinx_theme'

html_logo = "_static/ocf_tools_logo.png"
html_favicon = "_static/tamoc_favicon.ico"

html_sidebars = {
    "index": ["search-button-field"],
    "**": ["search-button-field", "sidebar-nav-bs"]
}

#html_theme = 'python_docs_theme'
html_title = ""

html_context = {
    "github_user": "socolofs",
    "github_repo": "ocf_tools",
    "github_version": "main",
    "doc_path": "doc",
}

rediraffe_redirects = {

}


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = ['scipy.css']

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "scipy": ("https://docs.scipy.org/doc/scipy", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
}

# based on numpy doc/source/conf.py
def linkcode_resolve(domain, info):
    """
    Determine the URL corresponding to Python object
    """
    if domain != "py":
        return None

    modname = info["module"]
    fullname = info["fullname"]

    submod = sys.modules.get(modname)
    if submod is None:
        return None

    obj = submod
    for part in fullname.split("."):
        try:
            obj = getattr(obj, part)
        except AttributeError:
            return None

    try:
        fn = inspect.getsourcefile(inspect.unwrap(obj))
    except TypeError:
        fn = None
    if not fn:
        return None

    try:
        source, lineno = inspect.getsourcelines(obj)
    except OSError:
        lineno = None

    if lineno:
        linespec = f"#L{lineno}-L{lineno + len(source) - 1}"
    else:
        linespec = ""

    fn = os.path.relpath(fn, start=os.path.dirname(ocf_tools.__file__))

    if "+" in ocf_tools.__version__:
        return f"https://github.com/socolofs/tamoc/tree/master/tamoc/{fn}{linespec}"
    else:
        return (
            f"https://github.com/socolofs/tamoc/tree/master/tamoc/{fn}{linespec}"
        )


def html_page_context(app, pagename, templatename, context, doctree):
    # Disable edit button for docstring generated pages
    if "generated" in pagename:
        context["theme_use_edit_page_button"] = False


def setup(app):
    app.connect("html-page-context", html_page_context)