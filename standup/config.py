import configparser

CONFIG_FILE = "config.ini"
DATA_FOLDER = "data"


def read_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config
