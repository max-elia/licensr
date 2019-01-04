# licensr
A command-line interface for easily licensing your project and make it compliant to the REUSE-Initiative's guidelines

---
[![reuse compliant](https://reuse.software/badge/reuse-compliant.svg)](https://reuse.software/)
[![PyPI](https://img.shields.io/pypi/v/licensr.svg?maxAge=3700)](http://pypi.python.org/pypi/licensr)
[![PyPI](https://img.shields.io/pypi/pyversions/licensr.svg?maxAge=3700)](http://pypi.python.org/pypi/licensr)

Making your project compliant to the guidelines of the [REUSE Initiative](https://reuse.software/) i.e. adding license and copyright information to every file in your project is an annoying process and can be quite tedious.

Licensr allows you to quickly add your chosen to your project from the command line. 
You just have to download the full license texts of your chosen licenses (and the one of your project's dependencies) and configure the config file to make the tool match your needs.

Don't see what you need?
[Open an issue](https://github.com/max-elia/licensr/issues/new)
to suggest any changes or improvements!

### Prerequisites

* Python 3.4+

### Installation

```bash
$ pip install licensr
```

Alternatively, grab the
[zip](https://github.com/max-elia/licensr/tarball/v0.1)!

### Usage

From the command line:

```bash
$ licensr -c "config file" -p "project name"
```

The arguments are optional and will default to "config.json" and the current working directory.

### Configuration

#license_text
The path to the file with the full license text. This file itself will be excluded from the licensing process. You are responsible for removing afterwards from your project.
Don't place your license_text files into the LICENSES folder, because it will be rewritten during the licensing.

#SPDX
The short identifier of the license.

## Source Code Header
#src_extensions_and_comment
You are required to add a comment-header to every source code file in your project. Therefore you have to specify under src_extensions_and_comment the src_extensions and the corresponding comment characters for every programming language used.
For the comments you can put either one (single-line comment), two (opening and closing) or three (opening - middle - closing) strings into a list.

#header
The header has to include a copyright notice and the SPDX Identifier of the license. In the config file it can be given as a path to a file or as string of the full header (be sure to include "\n")

For the src files this information is sufficient.
However we often don't have the ability to add the necessary information to every file for several reasons (e.g. binary files).
The [REUSE Initiative's practices](https://reuse.software/practices/2.0/) specify two other possibilities to add the licensing and copyright information also for those files.
* Debian File
	a file in the [DEP-5/copyright](https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/) file format
* .license File
	a file with the same name but the .license extension, containing the header.

## Debian File
For this method in addition to the SPDX we need:
#copyright
Year and Name of the copyright holder(s)

## .license File
For this method we only need the header.

#exceptions
If we have different licenses or copyright holders, we have to consider them in the exceptions. Here we have to specify the "path" variable for the desired directory or file. For the rest, based on which of the three preceding methods you want to use, you have to specify exactly the same options like before (except for the license_text, if the license is the same)

If more that one licensing-method is possible the order in which the methods are used is:
1. Source Code Header
2. Debian File
3. .license File

ATTENTION: The tool overwrites all old headers with the new ones. Be sure to save them if you need them.


### Contributing

I accept [pull requests](https://github.com/max-elia/licensr/compare);