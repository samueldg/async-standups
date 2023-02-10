import configparser
import os
import os.path
import stat
from pathlib import Path

from .templating import CONFIG_TEMPLATE

_SUBDIR = "standup"
_CONFIG_FILE = "config.ini"
_DATA_FOLDER = "data"


def _get_dir_path_from_env_var(env_var, fallback):
    """Read a directory path from an environment variable.

    If the env_var isn't defined, then use a fallback instead.
    The fallback value will be expanded if it contains an environment variable.
    """
    fallback_expanded = os.path.expandvars(fallback)
    dir_path = os.environ.get(env_var, fallback_expanded)
    return Path(dir_path)


# Trying to follow the XDG standards
# https://wiki.archlinux.org/title/XDG_Base_Directory

_CONFIG_HOME = _get_dir_path_from_env_var("XDG_CONFIG_HOME", "$HOME/.config")
_DATA_HOME = _get_dir_path_from_env_var("XDG_DATA_HOME", "$HOME/.local/share")

CONFIG_FILE = _CONFIG_HOME / _SUBDIR / _CONFIG_FILE
DATA_DIR = _DATA_HOME / _SUBDIR / _DATA_FOLDER


def read_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config


# TODO: Change this ridiculous interface for writing the config.
def write_config(token, username, icon_emoji):
    config = CONFIG_TEMPLATE.render(
        token=token,
        username=username,
        icon_emoji=icon_emoji,
    )
    with open(CONFIG_FILE, "x") as config_file:
        config_file.write(config)
    os.chmod(CONFIG_FILE, stat.S_IRUSR | stat.S_IWUSR)
