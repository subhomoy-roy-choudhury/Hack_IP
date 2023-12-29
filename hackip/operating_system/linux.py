import os
import socket
import re
from rich import print as rprint


class LinuxUtils(object):
    def __init__(self) -> None:
        self.os_name = "Linux Operating System"

    def prepare(self):
        pass

    def _output(self, data):
        try:
            hostname = socket.gethostname()  # returns hostname
            fqdn = socket.getfqdn(
                "www.google.com"
            )  # returns fully qualified domain name for name
            ip_address = socket.gethostbyname(
                hostname
            )  # returns IPv4 address with respect to hostname
            os.system("ip addr > out.txt")
            f = open("out.txt", "r")
            strings = re.findall(r"192.168.\d{1,3}.\d{1,3}", f.read())
            private_ip_addr = strings[-2]
            # HackIPUtility.output(
            #     system_data, hostname, ip_address, fqdn, private_ip_addr
            # )

        except Exception as e:
            rprint("[red]error while getting IP address or invalid hostname!")
