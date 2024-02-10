import yaml

def get_config():
    with open('config.yml', 'r') as file:
        configuration = yaml.safe_load(file)
        return configuration