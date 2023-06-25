
import os
import yaml

def load_command_map(directory):
    """
    Load command map from YAML files in the specified directory.

    Args:
        directory (str): The directory path containing the YAML files.

    Returns:
        dict: A dictionary representing the loaded command map.

    """
    command_map = {}
    for filename in os.listdir(directory):
        if filename.endswith(".yaml"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                file_commands = yaml.safe_load(file)
                command_map.update(file_commands)
    return command_map
