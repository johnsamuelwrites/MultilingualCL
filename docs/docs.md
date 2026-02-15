# MultilingualCL

## Documentation

This page summarizes how to run MultilingualCL and what to expect from it.

## Running The REPL

From the project root:

```bash
python -m multilingualcl.repl
```

The REPL reads natural-language requests and tries to resolve them to shell commands.

Examples:

- `list files`
- `show current directory`
- `create directory`

## How Command Resolution Works

MultilingualCL uses a fallback pipeline:

1. LLM-based intent extraction (if Ollama is enabled and reachable)
2. Rule-based semantic intent extraction
3. Static translation lookup in YAML resources

If no command can be resolved, it prints `Command not recognized.`.

## Safety And Preview

By default, the REPL:

- classifies command risk
- shows a preview before execution
- asks confirmation for risky commands

These behaviors are configurable using environment variables from [`../README.md`](../README.md).

## Supported Resources

Core resource files are stored under [`../resources/`](../resources):

- `en/actions.md` and `en/resources.md` for semantic matching
- `en/commands.yaml` and `fr/commandes.yaml` for command catalogs
- `yaml/command_map.yaml` for static command translations

## Platform Compatibility

The generated commands target Linux tools (`ls`, `grep`, `chmod`, etc.).
On Windows, run in WSL, Git Bash, or Linux containers for best results.

## Building Documentation From Scratch

Follow the instructions in [`build.md`](build.md).
