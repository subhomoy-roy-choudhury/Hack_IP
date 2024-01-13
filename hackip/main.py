import sys
import platform
from rich import print as rprint
from art import text2art

from hackip.logger_config import setup_logging
from hackip.helpers import create_folder
from hackip.constants import GENERATED_REPORT_FOLDER_NAME

from hackip.operating_system.linux import LinuxUtils
from hackip.operating_system.windows import WindowsUtils
from hackip.operating_system.macos import MacOSUtils

from hackip.chat import generate_response

# Setup logging
setup_logging()


class HackIP:
    def __init__(self):
        self.banner_text = "HackIP"

    def introduction(self):
        try:
            ascii_art = text2art(self.banner_text)
            rprint(f"[green]{ascii_art}")
        except Exception as e:
            print(f"Error in generating ASCII art: {e}")

    def get_os_utility(self):
        try:
            system_data = platform.uname()
            os_name = str(system_data.system).lower()

            if os_name == "windows":
                return WindowsUtils()
            elif os_name == "linux":
                return LinuxUtils()
            elif os_name == "darwin":
                return MacOSUtils()
            else:
                raise ValueError("Unsupported Operating System")
        except Exception as e:
            print(f"Error in detecting OS: {e}")
            sys.exit(1)

    def chat(self):
        while True:
            try:
                message = str(input("Hacker :- ")).strip()
                if message.lower() in ["quit", "exit"]:
                    print("Exiting chat.")
                    break

                try:
                    assistant_message = generate_response(message)
                    rprint(f"Assistant :- {assistant_message}")
                except Exception as e:
                    print(f"Error generating response: {e}")

            except KeyboardInterrupt:
                print("\nChat interrupted by user. Exiting...")
                break  # Use break instead of sys.exit(0) for cleaner exit

    def start(self):
        # self.introduction()
        create_folder(GENERATED_REPORT_FOLDER_NAME)

        os_object = self.get_os_utility()
        if os_object:
            os_object.stdout()

        self.chat()


def execute():
    try:
        HackIP().start()
    except Exception as e:
        print(f"Error during execution: {e}")


if __name__ == "__main__":
    execute()
