import os
import re
from hackip.operating_system.base import BaseOperatingSystemUtils

class LinuxUtils(BaseOperatingSystemUtils):
    def __init__(self) -> None:
        super().__init__()
        self.os_name = "Linux Operating System"

    def _get_private_ip_address(self):
        os.system("ip addr > out.txt")
        f = open("out.txt", "r")
        strings = re.findall(r"192.168.\d{1,3}.\d{1,3}", f.read())
        self.private_ip_addr = strings[-2]
        return self.private_ip_addr
