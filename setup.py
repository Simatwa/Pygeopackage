from setuptools import setup
from pygeo import __maintainer__,__email__,__repo__,__version__

setup(
    name="pygeogis",
    packages=["pygeo"],
    maintainer=__maintainer__,
    maintainer_email=__email__,
    version=__version__,
    url=__repo__,
    author=__maintainer__,
    install_requires=[
        "rasterio==1.3.6",
    ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    entry_points = {
        "console_scripts":[
            ("pygeogis = pygeo.main:main"),
        ],
    },
    classifiers = [
        "License :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.11",
    ],
)