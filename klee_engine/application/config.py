import os

BASE_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), "../", "../"))
ROOT_DIR = os.path.realpath(os.path.join(BASE_DIR, "../"))
CONFIG_DIR = os.path.realpath(os.path.join(ROOT_DIR, "conf/"))
CONFIG_NAMES = ("secrets.txt",)
SECRETS = {}

for config_filename in CONFIG_NAMES:
    config_file_path = os.path.realpath(os.path.join(CONFIG_DIR, config_filename))

    with open(config_file_path, "r") as f:
        for line in f.read().splitlines():
            key, value = line.split("=")
            key = key.replace(" ", "")
            value = value.replace(" ", "")
            SECRETS[key] = value
