import argparse
from command_map import load_command_map


def parse_user_command(command_map, current_locale, user_input):
    # Parse the user command using argparse and the command map
    parser = argparse.ArgumentParser()
    user_input_split = user_input.split()
    options_map = dict()

    # Find the command with matching name in the current locale
    matching_command = None
    for command_name, command_details in command_map.items():
        if command_details.get("locales", {}).get(current_locale):
            if user_input_split[0] in command_details.get("locales", {}).get(
                current_locale
            ).get("names", []):
                matching_command = command_details.get("locales", {}).get(
                    current_locale
                )
                break

    if matching_command:
        # Create a parser for the matching command
        subparsers = parser.add_subparsers(dest="command")
        command_parser = subparsers.add_parser(command_name)
        for translated_name in matching_command["names"]:
            if translated_name == user_input_split[0]:
                user_input = user_input.replace(
                    user_input_split[0], command_details["linux_command"], 1
                )  # Only the first occurence
                break

        # Add options for the command
        for option in matching_command.get("options", []):
            option_name = option["name"]
            option_aliases = option.get("aliases", [])

            options_map[option_name.replace("-", "")] = option_name
            for alias in option_aliases:
                options_map[alias.replace("-", "")] = option_name
            command_parser.add_argument(
                option_name, *option_aliases, action="store_true"
            )

        # Add subcommands for the command
        subcommand_parsers = command_parser.add_subparsers(dest="subcommand")
        for subcommand in matching_command.get("subcommands", []):
            subcommand_parser = subcommand_parsers.add_parser(subcommand["name"])

            # Add options for the subcommand
            for option in subcommand.get("options", []):
                option_name = option["name"]
                option_aliases = option.get("aliases", [])

                options_map[option_name.replace("-", "")] = option_name
                for alias in option_aliases:
                    options_map[alias.replace("-", "")] = option_name
                subcommand_parser.add_argument(
                    option_name, *option_aliases, action="store_true"
                )

        # Parse the user command with optional positional argument
        args_list = user_input.split()
        parsed_args, remaining = parser.parse_known_args(args_list)

        # Parse the positional argument separately if available
        if matching_command.get("positionals", []):
            # positionals = matching_command['positionals']
            if remaining:
                parsed_args.positional = remaining
                option_name = option["name"]

        # Parse the user command
        return parsed_args, options_map
