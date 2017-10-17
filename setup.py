#!/usr/bin/env python

from setuptools import setup
from lipsum3 import __version__


setup(
    name="lipsum3",
    version=__version__,
    description="Native Python3 lipsum generator",
    author="Eric Olson",
    author_email="reservoirdog@users.noreply.github.com",
    url="https://github.com/reservoirdog/lipsum3",
    packages="[lipsum3]",
    package_data={
        "lipsum3": [
            "data/*.txt"
        ]
    },
    classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: MacOS :: MacOS X',
          'Programming Language :: Python 3.6',
          'Topic :: Utilities'
          ],
)
