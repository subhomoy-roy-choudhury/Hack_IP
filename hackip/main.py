import platform

from hackip.operating_system.linux import LinuxUtils
from hackip.operating_system.windows import WindowsUtils
from hackip.operating_system.macos import MacOSUtils
from rich import print as rprint
from art import text2art
from rich.console import Console

from hackip.logger_config import setup_logging

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

    def start(self, *args, **kwargs):
        # Introduction
        self.introduction()

        # System Information
        os_object = self.get_os_utility()
        os_object.stdout()

def execute():
    HackIP().start()

if __name__ == "__main__":
    execute()