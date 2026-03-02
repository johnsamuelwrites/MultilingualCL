# MultilingualCL: Modernization Vision

## Context

MultilingualCL was conceived as a modern multilingual command line where everything -- commands, keywords, variable names, dates, numbers -- can be expressed in any language. First presented at [Capitole du Libre (2017)](https://doi.org/10.6084/m9.figshare.5661853.v1) and [DebConf20 (2020)](https://figshare.com/articles/presentation/Building_a_Multilingual_Command_Line/12857780), the project established strong conceptual foundations.

This document proposes a modernization vision that builds on those foundations and incorporates advances in LLMs, NLP, and modern development practices.

---

## What the Project Already Has

These existing assets are remarkably forward-looking and should be central to any modernization:

| Asset | File(s) | Value |
|-------|---------|-------|
| **Semantic action verb taxonomy** | `resources/en/actions.md` (300+ verbs in 30 categories) | Encodes the *intent* layer (create, delete, search, compress...) |
| **Resource type ontology** | `resources/en/resources.md` (50+ types) | Encodes the *target* layer (file, process, network, CPU, memory...) |
| **Action-resource composition** | `resources/actions.json`, `resources/commandline.json` | Maps verbs to valid resource targets (e.g., "create" -> [user, group, file, directory]) |
| **Full French translations** | `resources/fr/commandes.yaml` | Proof of concept for complete language coverage |
| **Command documentation** | `resources/en/commands.yaml` | Maps natural language descriptions to Linux commands |
| **428 language registry** | `languages.md` | Comprehensive language code catalog |
| **YAML command map schema** | `resources/yaml/command_map.yaml` | Extensible per-locale command definition format |
| **Object model** | `multilingualcl/model.py` | Clean class hierarchy (Command, Argument, SubCommand) |

---

## Current Limitations

### Architecture
- **Static 1:1 mapping**: Every command variant must be manually defined per language in YAML
- **No semantic understanding**: Parser does exact string matching only
- **Unused data**: Action verbs, resources, and French command docs are not connected to the runtime pipeline
- **Flat parsing**: argparse-based, cannot handle natural language or compositional commands
- **Single locale per session**: Detected from system locale, no runtime switching
- **No error intelligence**: Direct `subprocess.run()` with no output parsing or error recovery

### Code Quality
- **Incomplete parsing**: Positional argument handling is unfinished (`parser.py:67-72`)
- **No input sanitization**: Commands passed directly to subprocess
- **Hardcoded paths**: Resource loading uses relative paths
- **No caching**: Command map reloaded on every REPL iteration

---

## Modernization Vision

### Core Principle: Action + Resource + Modifier = Command

The project already has the ingredients for a **semantic command model**:

```
ACTION (verb)      + RESOURCE (noun)     + MODIFIER (adjective)  = LINUX COMMAND
────────────────     ─────────────────     ────────────────────     ─────────────
create               directory             -                        mkdir
delete               file                  force                    rm -f
list                 process               all                      ps aux
show                 memory                -                        free
search               file                  by name                  find . -name
compress             directory             recursive                tar -czvf
```

This already exists in the data (`actions.json` maps verbs to resources, `commands.yaml` maps descriptions to commands). The modernization is about **activating these connections** and making them multilingual and intelligent.

---

### Layer 1: LLM-Powered Intent Resolution

Replace static YAML lookup with semantic understanding.

**Current flow:**
```
user types "af -t" → exact match in YAML → "ls -a"
```

**Modern flow:**
```
user types "montre-moi les fichiers cachés"
  → language detection (French)
  → intent extraction: ACTION=list, RESOURCE=file, MODIFIER=hidden
  → command resolution: ls -la
  → safety check → execute
```

**Three-tier LLM strategy:**

| Tier | When | Model | Latency |
|------|------|-------|---------|
| **Local/fast** | Tab completion, known commands | Small model (<1B) or rule-based | <50ms |
| **Balanced** | Intent parsing, translation | Local 7B model (Ollama/llama.cpp) | <500ms |
| **Cloud** | Complex queries, error diagnosis, unknown languages | Claude/GPT API | 1-3s |

**Offline-first**: Core translation must work without internet. The existing YAML maps serve as the offline fallback, with LLM augmentation when available.

---

### Layer 2: Activate the Semantic Data

The existing `actions.md`, `resources.md`, `actions.json`, and `commandline.json` files should become the **knowledge graph** that powers command resolution:

1. **Action verb synonyms** (300+ verbs): Feed to the LLM as context so "erase", "remove", "delete", "wipe" all resolve to the DELETE action
2. **Resource types** (50+ types): Constrain what actions apply to what resources
3. **Action-resource combinations** (`actions.json`): Already maps which resources each action can target
4. **Command catalog** (`commands.yaml`): Already maps natural-language descriptions to actual commands

This transforms the multilingual pipeline from:
```
French YAML → English YAML → Linux Command
```

To:
```
Any Language → Action/Resource/Modifier (language-agnostic) → Linux Command
```

---

### Layer 3: Multilingual Expansion Strategy

**Current**: 2 locales, manual YAML translation per command per language.

**Proposed tiered approach:**

| Tier | Languages | Method | Quality |
|------|-----------|--------|---------|
| **Core** (5-10) | en, fr, es, zh, ar, hi, de, pt, ja, ko | Human-curated translations | Gold standard |
| **Community** (50+) | Languages with active contributors | Community translation + review | Verified |
| **LLM-generated** (428+) | All documented languages | LLM translation with confidence scores | Best-effort, marked as auto-translated |

**Key design decisions:**
- Translate **concepts** (action verbs, resource names), not individual command strings
- Use Unicode CLDR for locale data (dates, numbers, sorting)
- Support bidirectional text (Arabic, Hebrew) in terminal output
- Allow CJK input methods
- Respect cultural formatting (Arabic-Indic numerals, Chinese numerals, etc.)

---

### Layer 4: Modern REPL Experience

**Current**: Basic readline with termcolor.

**Proposed features:**

| Feature | Description |
|---------|-------------|
| **Rich TUI** | Syntax highlighting, tables, progress bars |
| **Intelligent autocomplete** | Context-aware suggestions based on action+resource model |
| **Fuzzy matching** | "commti" -> "Did you mean: commit?" (in user's language) |
| **Output translation** | Translate error messages and help text into user's language |
| **Command preview** | Show the actual Linux command before execution (transparency) |
| **Safety tiers** | Safe commands auto-execute; dangerous ones require confirmation |
| **Session memory** | Remember what user did earlier for contextual suggestions |
| **Multi-language mixing** | Handle code-switching (e.g., "git ajouter fichier.txt") |

---

### Layer 5: Safety and Transparency

**Current**: Direct `subprocess.run()` with no checks.

**Proposed risk-tiered execution:**

| Risk Level | Commands | Behavior |
|------------|----------|----------|
| **Safe** | ls, pwd, cat, git status | Execute, show output |
| **Moderate** | git commit, npm install, mv | Show preview, execute on enter |
| **Dangerous** | rm, chmod 777, git push -f | Explain impact in user's language, require "yes" |
| **Destructive** | rm -rf, mkfs, DROP TABLE | Double confirmation, show undo options |

**Dry-run mode**: Always available to preview what a command would do.

---

### Layer 6: Extensibility Architecture

**Current**: Monolithic YAML files.

**Proposed plugin system:**

- **Command packs**: Installable bundles (e.g., `multilingualcl-docker`, `multilingualcl-kubernetes`)
- **Language packs**: Community-contributed translation sets
- **Output formatters**: JSON, table, tree views
- **Shell integrations**: Bash/Zsh/Fish shell plugins
- **IDE integrations**: VS Code extension, JetBrains plugin

---

### Layer 7: Voice and Accessibility

- **Voice input**: Spoken commands in any language
- **Voice output**: Read results aloud (accessibility)
- **Screen reader support**: WCAG 2.1 AA compliance
- **High contrast mode**: For terminal accessibility

---

## Technical Modernization

| Component | Current | Proposed |
|-----------|---------|----------|
| Python version | 3.6+ | 3.11+ (pattern matching, better typing, tomllib) |
| Terminal UI | readline + termcolor | Rich/Textual/Prompt Toolkit |
| Parsing | argparse (static) | Semantic parser + LLM fallback |
| Config format | YAML only | TOML for config, YAML for command maps, JSON Schema validation |
| i18n framework | Custom locale detection | ICU via PyICU + Unicode CLDR |
| Testing | unittest | pytest + property-based testing (hypothesis) |
| Packaging | setup.py | pyproject.toml |
| CI/CD | GitHub Actions (basic) | Matrix testing (multiple Python versions, OSes) |
| Documentation | Sphinx (not built) | MkDocs Material with multilingual versions |

---

## Phased Roadmap

### Phase 1: Foundation (Activate Existing Data)
- Connect `actions.json`, `resources.md`, and `commands.yaml` to the runtime pipeline
- Build the Action + Resource + Modifier -> Command resolution engine
- Modernize REPL with Rich/Textual
- Add safety confirmation layer
- Expand command coverage to top 50 commands
- Add 3-5 more core languages (es, de, zh, ar, hi)

### Phase 2: Intelligence (Add LLM Layer)
- Integrate local LLM for intent parsing
- Add language auto-detection
- Implement fuzzy matching and smart suggestions
- Add output translation (error messages, help text)
- Build command preview/dry-run mode
- Session context and memory

### Phase 3: Ecosystem (Community and Extensibility)
- Plugin architecture for command packs and language packs
- Community translation platform
- Shell integrations (bash/zsh/fish)
- IDE extensions
- Voice input/output support

### Phase 4: Future (Advanced Capabilities)
- Multi-command workflows ("deploy to production" -> sequence of commands)
- Predictive commands (suggest before you ask)
- Cross-platform: Windows PowerShell translation, macOS compatibility
- Web-based terminal interface
- Mobile support (Termux, iSH)

---

## Key Insight

The most powerful idea in MultilingualCL is that **command-line operations are fundamentally language-agnostic actions on resources**. The project already encodes this in its action verbs, resource types, and composition rules. The modernization is not about starting over -- it is about activating the semantic framework that already exists and augmenting it with LLM intelligence for the languages and natural language understanding that static YAML cannot scale to cover.
