import os
import socket
from rich import print as rprint
from hackip.operating_system.base import BaseOperatingSystemUtils

class WindowsUtils(BaseOperatingSystemUtils):
    def __init__(self) -> None:
        super().__init__()
        self.os_name = "Windows Operating System"
    
    def _get_private_ip_address(self):
        self.private_ip_addr = socket.gethostbyname_ex(self.hostname)[-1][-1]
        return self.private_ip_addr