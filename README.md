# MultilingualCL

MultilingualCL is an interactive REPL that maps natural-language commands to shell commands.

## Quickstart

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

Optional LLM support (Ollama):

```bash
pip install -e ".[llm]"
```

### 3. Run the REPL

```bash
python -m multilingualcl.repl
```

Type a natural-language command, for example:

```text
list files
show current directory
create directory
```

Press `Ctrl+C` or `Ctrl+D` to exit.

## Configuration

The REPL behavior can be controlled through environment variables:

- `MULTILINGUALCL_LOCALE` (example: `en_US`, `fr_FR`)
- `MULTILINGUALCL_OLLAMA_ENABLED` (`true`/`false`)
- `MULTILINGUALCL_OLLAMA_MODEL` (default: `mistral`)
- `MULTILINGUALCL_OLLAMA_TIMEOUT` (seconds, default: `10.0`)
- `MULTILINGUALCL_SAFETY_ENABLED` (`true`/`false`)
- `MULTILINGUALCL_SHOW_PREVIEW` (`true`/`false`)

Example:

```bash
MULTILINGUALCL_LOCALE=fr_FR MULTILINGUALCL_OLLAMA_ENABLED=false python -m multilingualcl.repl
```

## Platform notes

- Generated commands are Linux-oriented (`ls`, `grep`, `chmod`, etc.).
- On Windows, many commands will not exist unless you run in WSL, Git Bash, or a Linux container.

## Tests

Run all tests:

```bash
python -m tests.tests
```

Run coverage:

```bash
coverage run --source=multilingualcl -m unittest tests.tests
coverage report -m
```

Note: some tests execute shell commands (for example `ls`) and may fail on native Windows shells.

## Documentation

- Docs index: [`docs/README.md`](docs/README.md)
- Detailed docs: [`docs/docs.md`](docs/docs.md)
- Build docs: [`docs/build.md`](docs/build.md)

## Author

- John Samuel

## Talks

- [Rethinking the command line](https://2017.capitoledulibre.org/programme/#schedule), Capitole du Libre, Toulouse, France, November 19, 2017, [Slides](https://doi.org/10.6084/m9.figshare.5661853.v1)
- [Building a Multilingual Command Line](https://debconf20.debconf.org/talks/45-building-a-multilingual-command-line/), Debian Conference (DebConf20), August 25, 2020, [Slides](https://figshare.com/articles/presentation/Building_a_Multilingual_Command_Line/12857780)

## License

The code is released under GPLv3+.
Documentation and other content are released under [CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/).

