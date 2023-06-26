from parser import parse_user_command


def obtain_command_from_translation(command_map, current_locale, user_input):
    parsed_args, options_map = parse_user_command(
        command_map, current_locale, user_input
    )
    unparsed_args = []  # Add the command name
    for arg in vars(parsed_args):
        value = getattr(parsed_args, arg)
        if value is not None:
            if isinstance(value, bool):  # Handle boolean flags without values
                if value and arg in options_map:
                    option = options_map[arg]
                    unparsed_args.append(f"{option}")
            else:
                if type(value) == list:
                    unparsed_args.append(" ".join(value))
                else:
                    unparsed_args.append(str(value))

    command_string = " ".join(unparsed_args)

    return command_string
