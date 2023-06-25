import readline
import difflib
from termcolor import colored

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
    matches = difflib.get_close_matches(text, options, n=5, cutoff=0.5)  # Limit suggestions to 5 and set cutoff threshold
    return matches

def highlight_match(text, match):
    highlighted_text = colored(match, "yellow")
    return text.replace(match, highlighted_text)

def evaluate_command(command):
    # TODO: Add your logic to evaluate the command here
    return "Result: " + command

def repl():
    while True:
        try:
            command = input(colored(">>> ", "cyan"))  # Prompt in cyan color
            if command.strip() == "":
                continue

            save_history()

            # Autocorrection
            suggestions = get_suggestions(command, ["help", "quit"])  # Example options
            if suggestions:
                suggestion = suggestions[0]
                if suggestion != command: 
                  corrected_command = input(colored(
                      f"Did you mean '{highlight_match(suggestion, command)}'? [Y/n] ", "magenta"))
                  if corrected_command.lower() == "y":
                      command = suggestion

            # Autocompletion
            completer = readline.get_completer()
            if completer:
                completed_command = completer(command, 0)
                if completed_command != command:
                    command = completed_command

            # Evaluation
            result = evaluate_command(command)
            print(colored(result, "green"))  # Print result in green color

        except (KeyboardInterrupt, EOFError):
            print(colored("\nExiting REPL...", "red"))
            break

if __name__ == "__main__":
    initialize()
    repl()

