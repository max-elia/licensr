# Copyright (c) 2019 Max Elia Schweigkofler <schweigkofler.max@gmail.com>, Andrea Janes <ajanes@unibz.it>
# 
# This file is part of the project reuse-checker which is released under the MIT license.
# See file LICENSE or go to https://github.com/max-elia/licensr for full license details.
# 
# SPDX-License-Identifier: MIT
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="licensr",
    version="0.1.1",
    author="Max Elia Schweigkofler",
    author_email="schweigkofler.max@gmail.com",
    description="A CLI for licensing your project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/max-elia/licensr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': [
            'licensr = licensr.licensr:main'
        ]
    },
    keywords="licenser licensing reuse open source",
)