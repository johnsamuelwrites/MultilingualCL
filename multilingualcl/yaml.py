import yaml

def read_config(command):
  print(yaml.dump(command, allow_unicode=True))
