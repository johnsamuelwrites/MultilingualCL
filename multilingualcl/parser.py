import argparse
from command_map import load_command_map


def parse_user_command(command_map, current_locale, user_input):
    # Parse the user command using argparse and the command map
    parser = argparse.ArgumentParser()
    user_input_split = user_input.split()

    # Find the command with matching name in the current locale
    matching_command = None
    for command_name, command_details in command_map.items():
        if command_details.get('locales', {}).get(current_locale):
            if user_input_split[0] in command_details.get('locales', {}).get(current_locale).get("names", []):
               matching_command = command_details.get('locales', {}).get(current_locale)
               break

    if matching_command:
        # Create a parser for the matching command
        subparsers = parser.add_subparsers(dest='command')
        command_parser = subparsers.add_parser(command_name)

        # Add options for the command
        for option in matching_command.get('options', []):
            option_name = option['name']
            option_aliases = option.get('aliases', [])
            command_parser.add_argument(option_name, *option_aliases, action='store_true')

        # Add subcommands for the command
        subcommand_parsers = command_parser.add_subparsers(dest='subcommand')
        for subcommand in matching_command.get('subcommands', []):
            subcommand_parser = subcommand_parsers.add_parser(subcommand['name'])

            # Add options for the subcommand
            for option in subcommand.get('options', []):
                option_name = option['name']
                option_aliases = option.get('aliases', [])
                subcommand_parser.add_argument(option_name, *option_aliases, action='store_true')

        # Parse the user command with optional positional argument
        args_list = user_input.split()
        parsed_args, remaining = parser.parse_known_args(args_list)
    
        # Parse the positional argument separately if available
        if matching_command.get('positionals', []):
            #positionals = matching_command['positionals']
            if remaining: 
                parsed_args.positional = remaining 

        # Parse the user command
        #parsed_args = parser.parse_args(user_input.split())
        return parsed_args




# Example usage
command_map_directory = "../resources/yaml"  # Specify the path to the reference YAML file
command_map = load_command_map(command_map_directory)

current_locale = "en_US"
user_input = input("Enter the command: ")
parsed_command = parse_user_command(command_map, current_locale, user_input)
print(parsed_command)

