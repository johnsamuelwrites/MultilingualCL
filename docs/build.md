# MultilingualCL
## Building Documentation

Run the following command to first install the necessary packages for the generation of documentation. `sphinx` is used for managing the documentation.
``
$ pip install -r requirements.txt
``

Once all the necessary packages are installed, run the following command.
``
$ sphinx-build -b html docs/ build/html
``

The HTML documentation is available in `build/html/` folder.

Some documentation is also in `markdown` format and can be converted to `restructuredText` in the following way.
``
pandoc --from=markdown --to=rst --output=README.rst README.md
``

Check documentation [here](docs.md).

## Building Documentation from Scratch
### Building Templates
For generating documentation, `sphinx` is used.  In order to obtain the basic templates of `multilingualcl` documentation, run the following command.

``
sphinx-apidoc -o docs multilingualcl/
``

This will generate the following documentation files.
``
Creating file docs/multilingualcl.rst.
Creating file docs/modules.rst.
``

Now, in order to generate the configuration for generating documentation by `sphinx`, the next step is to use `sphinx-quickstart`.

``
$ sphinx-quickstart

Welcome to the Sphinx 3.0.4 quickstart utility.

Please enter values for the following settings (just press Enter to
accept a default value, if one is given in brackets).

Selected root path: .

You have two options for placing the build directory for Sphinx output.
Either, you use a directory "_build_" within the root path, or you separate
"source" and "build" directories within the root path.
> Separate source and build directories (y/n) [n]: y

The project name will occur in several places in the built documentation.
> Project name: multilingualcl
> Author name(s): John Samuel
> Project release []: v0.1

If the documents are to be written in a language other than English,
you can select a language here by its language code. Sphinx will then
translate text that it generates into that language.

For a list of supported codes, see
https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-language.
> Project language [en]: en

Creating file ./source/conf.py.
Creating file ./source/index.rst.
Creating file ./Makefile.
Creating file ./make.bat.

Finished: An initial directory structure has been created.

You should now populate your master file ./source/index.rst and create other documentation
source files. Use the Makefile to build the docs, like so:
   make builder
where "builder" is one of the supported builders, e.g. html, latex or linkcheck.

``

Now run the following command to generate HTML files for the documentation
``
make html

``

This will generate the HTML files in `build/html`. 

### Modifications
For modifications like changing the theme, check the file `source/conf.py`. For changing the documentation, change the files `*.rst` (written in `restructuredText` format).
