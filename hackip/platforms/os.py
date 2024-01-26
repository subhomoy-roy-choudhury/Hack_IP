import os
import re
import socket

from .base import BaseOperatingSystem


class UnixLikeOS(BaseOperatingSystem):
    def __init__(self, cuttly_api_key, advanced_scanning, os_name) -> None:
        super().__init__(cuttly_api_key, advanced_scanning)
        self.os_name = os_name

    def _get_private_ip_address(self):
        # The function creates a socket that connects to a remote server on the Internet
        # This is used to determine the local machine's IP address on the network.
        try:
            # This is a dummy connection, it doesn't need to succeed
            # 1.1.1.1 is a public DNS server provided by Cloudflare
            # 80 is the standard HTTP port
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("1.1.1.1", 80))
                return s.getsockname()[0]
        except Exception as e:
            return f"Error: {e}"


class WindowsOS(BaseOperatingSystem):
    def __init__(self, cuttly_api_key, advanced_scanning) -> None:
        super().__init__(cuttly_api_key, advanced_scanning)
        self.os_name = "Windows Operating System"

    def _get_private_ip_address(self):
        return socket.gethostbyname(self.hostname)


class LinuxOS(UnixLikeOS):
    def __init__(self, cuttly_api_key, advanced_scanning) -> None:
        super().__init__(cuttly_api_key, advanced_scanning, "Linux Operating System")


class MacOS(UnixLikeOS):
    def __init__(self, cuttly_api_key, advanced_scanning) -> None:
        super().__init__(cuttly_api_key, advanced_scanning, "Mac Operating System")
