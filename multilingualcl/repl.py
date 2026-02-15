import readline
import difflib
from termcolor import colored
import locale
import subprocess
from multilingualcl.command_map import load_command_map
from multilingualcl.command import obtain_command_from_translation
from multilingualcl.semantic import (
    SemanticIndex, extract_intent_rulebased, resolve_command,
)
from multilingualcl.safety import classify_risk, confirm_execution, RiskLevel
from multilingualcl.config import load_config

# Optional rich import -- fall back to termcolor if unavailable
try:
    from rich.console import Console
    from rich.panel import Panel
    _RICH_AVAILABLE = True
except ImportError:
    _RICH_AVAILABLE = False

# Optional LLM import
try:
    from multilingualcl.llm import LLMEngine, is_ollama_available
    _LLM_AVAILABLE = True
except ImportError:
    _LLM_AVAILABLE = False

HISTORY_FILE = ".repl_history"  # File to store command history


def load_history():
    try:
        readline.read_history_file(HISTORY_FILE)
    except FileNotFoundError:
        pass


def save_history():
    readline.write_history_file(HISTORY_FILE)


def initialize():
    load_history()
    readline.parse_and_bind("tab: complete")  # Enable tab completion
    readline.set_auto_history(True)  # Enable command history


def get_suggestions(text, options):
    matches = difflib.get_close_matches(
        text, options, n=2, cutoff=0.5
    )  # Limit suggestions to 2 and set cutoff threshold
    return matches


def highlight_match(text, match):
    highlighted_text = colored(match, "yellow")
    return text.replace(match, highlighted_text)


def evaluate_command(command, command_map, current_locale):
    real_command = obtain_command_from_translation(command_map, current_locale, command)
    subprocess.run(real_command.split())
    return "Result: " + real_command


def evaluate_command_v2(user_input, semantic_index, config,
                        llm_engine=None, command_map=None,
                        current_locale=None, console=None):
    """New evaluation pipeline with fallback chain.

    Tier 1: LLM-based intent extraction (if Ollama available)
    Tier 2: Rule-based semantic extraction (action+resource matching)
    Tier 3: Static YAML match (existing behavior)
    Then: safety check -> preview -> execute
    """
    intent = None
    linux_command = None

    # Tier 1: LLM (optional)
    if (llm_engine is not None and _LLM_AVAILABLE
            and is_ollama_available()):
        try:
            intent = llm_engine.extract_intent(
                user_input, current_locale, semantic_index
            )
        except Exception:
            intent = None

    # Tier 2: Rule-based semantic
    if intent is None or intent.confidence < 0.5:
        semantic_intent = extract_intent_rulebased(
            user_input, semantic_index, current_locale
        )
        if intent is None or semantic_intent.confidence > intent.confidence:
            intent = semantic_intent

    # Resolve intent to command if we got a good match
    if intent is not None and intent.confidence >= 0.5:
        linux_command = resolve_command(intent, semantic_index)

    # Tier 3: Static YAML match (existing behavior) as fallback
    if linux_command is None and command_map is not None:
        try:
            linux_command = obtain_command_from_translation(
                command_map, current_locale, user_input
            )
        except Exception:
            linux_command = None

    if not linux_command:
        _print_message(console, "Command not recognized.", style="error")
        return None

    # Safety check
    if config.safety_enabled:
        safety = classify_risk(linux_command)

        # Preview
        if config.show_command_preview:
            _print_preview(console, linux_command, safety)

        # Confirm if needed
        if safety.requires_confirm:
            if not confirm_execution(safety):
                _print_message(console, "Cancelled.", style="warning")
                return None
    elif config.show_command_preview:
        _print_message(console, f"  {linux_command}", style="info")

    # Execute
    subprocess.run(linux_command.split())
    return linux_command


def _print_preview(console, command, safety):
    """Display command preview with risk indicator."""
    risk_colors = {
        RiskLevel.SAFE: "green",
        RiskLevel.MODERATE: "yellow",
        RiskLevel.DANGEROUS: "red",
        RiskLevel.DESTRUCTIVE: "bright_red",
    }
    color = risk_colors.get(safety.risk_level, "white")

    if console and _RICH_AVAILABLE:
        console.print(Panel(
            f"[bold]{command}[/bold]",
            title=f"[{color}]{safety.risk_level.value.upper()}[/{color}]",
            border_style=color,
        ))
    else:
        label = safety.risk_level.value.upper()
        print(colored(f"  [{label}] {command}", color))


def _print_message(console, text, style="info"):
    """Print a styled message."""
    color_map = {
        "error": "red",
        "warning": "yellow",
        "info": "cyan",
        "success": "green",
    }
    color = color_map.get(style, "white")

    if console and _RICH_AVAILABLE:
        console.print(f"[{color}]{text}[/{color}]")
    else:
        print(colored(text, color))


def repl():
    config = load_config()

    # Determine locale
    current_locale = config.locale_override or locale.getlocale()[0]

    # Load resources once at startup
    command_map = load_command_map()
    semantic_index = SemanticIndex()
    semantic_index.load()

    # Initialize console
    console = None
    if _RICH_AVAILABLE:
        console = Console()

    # Initialize LLM engine if available and enabled
    llm_engine = None
    if _LLM_AVAILABLE and config.ollama_enabled:
        llm_engine = LLMEngine(model_name=config.ollama_model)

    while True:
        try:
            command = input(colored(">>> ", "cyan"))
            if command.strip() == "":
                continue

            save_history()

            result = evaluate_command_v2(
                command, semantic_index, config,
                llm_engine=llm_engine,
                command_map=command_map,
                current_locale=current_locale,
                console=console,
            )
            if result:
                _print_message(console, f"Result: {result}", style="success")

        except (KeyboardInterrupt, EOFError):
            _print_message(console, "\nExiting REPL...", style="error")
            break


if __name__ == "__main__":
    initialize()
    repl()
