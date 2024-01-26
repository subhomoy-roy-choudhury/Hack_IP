import configparser

from .constants import (
    CONFIGURATION_FILE_PATH,
    CONFIGURATION_SECTION_KEYS,
    CREDENTIALS_KEYS,
)
from .helpers import get_status_symbol, file_exists
from rich import print as rprint


def load_configuration():
    if not file_exists(CONFIGURATION_FILE_PATH):
        rprint("[red]Configuration File Not Found[/red]")
        return

    config = configparser.ConfigParser()
    # Read the config.ini file
    config.read(CONFIGURATION_FILE_PATH)
    rprint("[yellow] Credentials [/yellow]")

    # Validate Configuration file
    if config.has_section(CONFIGURATION_SECTION_KEYS.CREDENTIALS.value):
        for key in CREDENTIALS_KEYS:
            if config.has_option(
                CONFIGURATION_SECTION_KEYS.CREDENTIALS.value, key.value[0]
            ):
                rprint(f"{get_status_symbol('pass')} {key.value[1]} Found")
            else:
                rprint(f"{get_status_symbol('fail')} {key.value[1]} Not Found")
    else:
        rprint("[red]Credentials section not found in the configuration file.[/red]")

    return config
