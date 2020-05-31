#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import setuptools,runpy

version_meta = runpy.run_path("./multilingualcl/version.py")
VERSION = version_meta["__version__"]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="multilingualcl",
    version=VERSION,
    author="John Samuel",
    author_email="johnsamuelwrites@example.com",
    description="Building multilingual command line",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johnsamuelwrites/MultilingualCL",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'Markdown>=3.2.2',
        'pyyaml>=5.3.1',
    ],
    python_requires='>=3.6',
)
