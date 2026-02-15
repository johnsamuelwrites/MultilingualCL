# MultilingualCL
## Building Documentation

Install documentation dependencies:

```bash
pip install -r requirements.txt
```

Generate HTML documentation:

```bash
sphinx-build -b html docs/ build/html
```

The generated site is in `build/html/`.

Some files are in Markdown. If needed, convert them to reStructuredText:

```bash
pandoc --from=markdown --to=rst --output=README.rst README.md
```

See [`docs.md`](docs.md) for usage-oriented docs.

## Building Documentation from Scratch
### Building Templates
To regenerate API template files:

```bash
sphinx-apidoc -o docs multilingualcl/
```

This generates files such as:

```
Creating file docs/multilingualcl.rst.
Creating file docs/modules.rst.
```

To bootstrap a brand-new Sphinx config:

```bash
sphinx-quickstart
```

Then generate HTML:

```bash
sphinx-build -b html docs/ build/html
```

### Modifications

For theme or extension changes, edit [`conf.py`](conf.py).
For content changes, edit the files in `docs/` (`.rst` and `.md`).
