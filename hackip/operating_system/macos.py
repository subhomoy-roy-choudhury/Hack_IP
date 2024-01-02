import os, re
import socket
import psutil
from rich import print as rprint
from operating_system.base import BaseOperatingSystemUtils


class MacOSUtils(BaseOperatingSystemUtils):
    def __init__(self) -> None:
        super().__init__()
        self.os_name = "Mac Operating System"
    
    def _get_private_ip_address(self):
        self.private_ip_addr = socket.gethostbyname_ex(self.hostname)[-1][0]
        return self.private_ip_addr