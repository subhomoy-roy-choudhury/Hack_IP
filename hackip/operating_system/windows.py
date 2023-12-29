import os
import socket
from rich import print as rprint

class WindowsUtils(object):
    def __init__(self) -> None:
        self.os_name = "Windows Operating System"

    def prepare(self):
        pass

    def _output(self, data):
        try:
            hostname = socket.gethostname()  # returns hostname
            ip_address = socket.gethostbyname(
                hostname
            )  # returns IPv4 address with respect to hostname
            fqdn = socket.getfqdn(
                "www.google.com"
            )  # returns fully qualified domain name for name
            private_ip_addr = socket.gethostbyname_ex(hostname)[-1][-1]
            # HackIPUtility.output(
            #     system_data, hostname, ip_address, fqdn, private_ip_addr
            # )
        except Exception as e:
            rprint("[red]error while getting IP address or invalid hostname!")
