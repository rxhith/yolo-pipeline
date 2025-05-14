import setuptools
from setuptools import find_packages

__version__ = "0.0.0.1"

REPO_NAME = "Agrix"
AUTHOR_NAME = "Abhinand"
SRC_REPO = "agrix"

setuptools.setup(
    name=REPO_NAME,
    version=__version__,
    author=AUTHOR_NAME,
    package_dir={"":"src"},
    packages = find_packages(where="src"),

)