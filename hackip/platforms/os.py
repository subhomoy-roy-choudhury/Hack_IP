import os
import socket
import re
from hackip.platforms.base import BaseOperatingSystemUtils

class WindowsUtils(BaseOperatingSystemUtils):
    def __init__(self, cuttly_api_key) -> None:
        super().__init__(cuttly_api_key)
        self.os_name = "Windows Operating System"
    
    def _get_private_ip_address(self):
        self.private_ip_addr = socket.gethostbyname_ex(self.hostname)[-1][-1]
        return self.private_ip_addr
    
class LinuxUtils(BaseOperatingSystemUtils):
    def __init__(self, cuttly_api_key) -> None:
        super().__init__(cuttly_api_key)
        self.os_name = "Linux Operating System"

    def _get_private_ip_address(self):
        os.system("ip addr > out.txt")
        f = open("out.txt", "r")
        strings = re.findall(r"192.168.\d{1,3}.\d{1,3}", f.read())
        self.private_ip_addr = strings[-2]
        return self.private_ip_addr
    
class MacOSUtils(BaseOperatingSystemUtils):
    def __init__(self, cuttly_api_key) -> None:
        super().__init__(cuttly_api_key)
        self.os_name = "Mac Operating System"
    
    def _get_private_ip_address(self):
        self.private_ip_addr = socket.gethostbyname_ex(self.hostname)[-1][0]
        return self.private_ip_addr
