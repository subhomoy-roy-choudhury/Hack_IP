import socket
import psutil
from rich import print as rprint
from operating_system.base import BaseOperatingSystemUtils


class MacOSUtils(BaseOperatingSystemUtils):
    def __init__(self) -> None:
        super().__init__()
        self.os_name = "Mac Operating System"
        self.hostname = socket.gethostname()  # returns hostname
        self.fqdn = socket.getfqdn(
            "www.google.com"
        )  # returns fully qualified domain name for name
        self.ip_address = socket.gethostbyname(
            self.hostname
        )  # returns IPv4 address with respect to hostname
        self.private_ip_addr = socket.gethostbyname_ex(self.hostname)[-1][-1]

    def prepare(self):
        result = {}
        result["System Information"] = {
            **self._format_system_info(),
            "Boot Time": self._format_boot_time(),
        }
        result["CPU Information"] = self._format_cpu_information()
        result["Memory Information"] = self._format_memory_information()

        return result
