import argparse
import logging
import platform
import sys

from art import text2art
from .chat import generate_response
from .constants import (
    CONFIGURATION_SECTION_KEYS,
    CREDENTIALS_KEYS,
    GENERATED_REPORT_FOLDER_NAME,
)
from .helpers import create_folder
from .logger_config import setup_logging
from .platforms.os import LinuxOS, MacOS, WindowsOS
from rich import print as rprint
from .utils import load_configuration

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


class HackIP:
    BANNER_TEXT = "HackIP"

    def __init__(self, configuration, advanced_scanning=False):
        self.configuration = configuration
        self.advanced_scanning = advanced_scanning

    def introduction(self):
        try:
            ascii_art = text2art(HackIP.BANNER_TEXT)
            rprint(f"[green]{ascii_art}")
        except Exception as e:
            print(f"Error in generating ASCII art: {e}")

    def get_os_utility(self):
        os_name = platform.system().lower()
        os_util_class = {
            "windows": WindowsOS,
            "linux": LinuxOS,
            "darwin": MacOS,
        }.get(os_name)

        if os_util_class is None:
            rprint("[red]Unsupported Operating System[/red]")
            sys.exit(1)

        try:
            cuttly_api_key = self.configuration.get(
                CONFIGURATION_SECTION_KEYS.CREDENTIALS.value,
                CREDENTIALS_KEYS.CUTTLY_API_KEY.value[0],
            )
        except Exception as e:
            cuttly_api_key = None

        try:
            if cuttly_api_key is None:
                logger.warning("Cuttly API key not found in configuration.")

            return os_util_class(
                cuttly_api_key=cuttly_api_key, advanced_scanning=self.advanced_scanning
            )

        except Exception as e:
            rprint(f"[red]Error while initializing OS utility: {e}[/red]")
            sys.exit(1)

    def chat(self):
        try:
            openai_key = self.configuration.get(
                CONFIGURATION_SECTION_KEYS.CREDENTIALS.value,
                CREDENTIALS_KEYS.OPENAI_API_KEY.value[0],
            )
        except Exception as _:
            rprint("[red]Error finding OpenAI API key[/red]")
            return

        while True:
            try:
                message = input("Hacker :- ").strip()
                if message.lower() in ["quit", "exit"]:
                    print("Exiting chat.")
                    break

                assistant_message = generate_response(openai_key, message)
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
        parser = argparse.ArgumentParser(
            description="This is a tool to get IP and system information of a specific device"
        )

        # Add subparsers for the 'run' and 'chat' commands
        subparsers = parser.add_subparsers(dest="command", help="Sub-command help")

        # Create the parser for the "run" command
        parser_run = subparsers.add_parser("run", help="Start Execution")
        parser_run.add_argument(
            "-d",
            "--details",
            action="store_true",
            help="Advanced Nmap Scanning of open ports",
        )

        # Create the parser for the "chat" command
        parser_chat = subparsers.add_parser(
            "chat", help="Start Chatting with your details report"
        )
        parser_chat.add_argument("--verbose", action="store_true", help="Verbose mode")

        args = parser.parse_args()

        # Now you can check if 'run' or 'chat' was called, and if '--details' was used
        if args.command == "run":
            rprint("[green]Start Execution...[/green]\n")
            # Load configuration
            configuration = load_configuration()

            # Start HackIP
            HackIP(configuration, args.details).start()

        elif args.command == "chat":
            rprint("[green]Chatting with details...[/green]\n")
            # Add OpenAI LLM Conversation

    except Exception as e:
        print(f"Error during execution: {e}")
