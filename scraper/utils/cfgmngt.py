import os
import yaml

def get_config():
    config = {}
    if 'config.yml' in os.listdir():
        with open("config.yml", "r") as f:
            config = yaml.safe_load(f)
    else:
        print("No config file found")
        exit(1)
    return config