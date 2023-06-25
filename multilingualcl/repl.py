import readline
import difflib
from termcolor import colored
import locale
from command_map import load_command_map
from parser import parse_user_command

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

def evaluate_command(command, command_map, current_locale):
    print(command)
    parsed_command = parse_user_command(command_map, current_locale, command)
    print(parsed_command)

    return "Result: " + command

def repl():
    while True:
        try:
            current_locale = locale.getlocale()[0]
            command_map = load_command_map()

            command = input(colored(">>> ", "cyan"))  # Prompt in cyan color
            if command.strip() == "":
                continue

            save_history()


            # Evaluation
            result = evaluate_command(command, command_map, current_locale)
            print(result)
            print(colored(result, "green"))  # Print result in green color

        except (KeyboardInterrupt, EOFError):
            print(colored("\nExiting REPL...", "red"))
            break

if __name__ == "__main__":
    initialize()
    repl()

