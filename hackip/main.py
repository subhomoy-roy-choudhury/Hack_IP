import sys
import platform
import logging
from rich import print as rprint
from art import text2art

from hackip.logger_config import setup_logging
from hackip.helpers import create_folder
from hackip.constants import (
    GENERATED_REPORT_FOLDER_NAME,
    CONFIGURATION_SECTION_KEYS,
    CREDENTIALS_KEYS,
)

from hackip.operating_system.linux import LinuxUtils
from hackip.operating_system.windows import WindowsUtils
from hackip.operating_system.macos import MacOSUtils

from hackip.chat import get_client, generate_response
from hackip.utils import load_configuration

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


class HackIP:
    BANNER_TEXT = "HackIP"

    def __init__(self, configuration):
        self.configuration = configuration

    def introduction(self):
        try:
            ascii_art = text2art(HackIP.BANNER_TEXT)
            rprint(f"[green]{ascii_art}")
        except Exception as e:
            print(f"Error in generating ASCII art: {e}")

    def get_os_utility(self):
        os_name = platform.system().lower()
        os_util_class = {
            "windows": WindowsUtils,
            "linux": LinuxUtils,
            "darwin": MacOSUtils,
        }.get(os_name)

        if os_util_class is None:
            rprint("[red]Unsupported Operating System[/red]")
            sys.exit(1)

        try:
            cuttly_api_key = self.configuration.get(
                CONFIGURATION_SECTION_KEYS.CREDENTIALS.value,
                CREDENTIALS_KEYS.CUTTLY_API_KEY.value[0],
            )
            if cuttly_api_key is None:
                logger.warning("Cuttly API key not found in configuration.")

            return os_util_class(cuttly_api_key=cuttly_api_key)

        except Exception as e:
            rprint(f"[red]Error while initializing OS utility: {e}[/red]")
            sys.exit(1)

    def chat(self):
        openai_key = self.configuration.get(
            CONFIGURATION_SECTION_KEYS.CREDENTIALS.value,
            CREDENTIALS_KEYS.OPENAI_API_KEY.value[0],
        )
        if not openai_key:
            rprint("[red]Error finding OpenAI API key[/red]")
            return

        while True:
            try:
                message = input("Hacker :- ").strip()
                if message.lower() in ["quit", "exit"]:
                    print("Exiting chat.")
                    break

                client = get_client(api_key=openai_key)
                assistant_message = generate_response(client, message)
                rprint(f"Assistant :- {assistant_message}")

            except KeyboardInterrupt:
                print("\nChat interrupted by user. Exiting...")
                break
            except Exception as e:
                rprint(f"[red]Error: {e}[/red]")

    def start(self):
        # self.introduction()
        create_folder(GENERATED_REPORT_FOLDER_NAME)

        os_object = self.get_os_utility()
        if os_object:
            os_object.stdout()

        self.chat()


def execute():
    try:
        # Load configuration
        configuration = load_configuration()
        # Start HackIP
        HackIP(configuration).start()
    except Exception as e:
        print(f"Error during execution: {e}")


if __name__ == "__main__":
    execute()
