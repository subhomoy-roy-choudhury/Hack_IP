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


class HackIP(object):
    def __init__(self) -> None:
        self.banner_text = "HackIP"

    def introduction(self):
        # Generate ASCII art text
        ascii_art = text2art(self.banner_text)

        # Print using rich for colored output
        rprint(f"[green]{ascii_art}")

    def get_os_utility(self):
        system_data = platform.uname()
        os_name = str(system_data.system)

        if os_name.lower() == "windows":
            return WindowsUtils()

        elif os_name.lower() == "linux":
            return LinuxUtils()

        elif os_name.lower() == "darwin":
            return MacOSUtils()

        else:
            raise Exception("Invalid Operating System")

    def check_configuration(self):
        pass

    def chat(self):
        while True:
            message = str(input("Hacker :- "))
            if message.lower() == "quit":
                break
            assistant_message=generate_response(message)
            print(f"Assistant :- {assistant_message}")
        

    def start(self, *args, **kwargs):
        # Introduction
        # self.introduction()

        # Create Reports Folder
        create_folder(GENERATED_REPORT_FOLDER_NAME)

        # System Information
        os_object = self.get_os_utility()
        os_object.stdout()

        # Chat with data
        self.chat()


def execute():
    HackIP().start()


if __name__ == "__main__":
    execute()
