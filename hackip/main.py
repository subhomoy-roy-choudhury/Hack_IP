import socket, os, re, platform
from .utils.base import HackIPUtility
from rich import print as rprint
from rich.console import Console

class HackIP(object):
    def __init__(self) -> None:
        pass
    
    def _windows(self,system_data):
        rprint("[yellow]---------------------------Windows-------------------------------")
        try:

            hostname = socket.gethostname() # returns hostname
            ip_address = socket.gethostbyname(hostname)  # returns IPv4 address with respect to hostname
            fqdn = socket.getfqdn('www.google.com') # returns fully qualified domain name for name
            private_ip_addr = socket.gethostbyname_ex(hostname)[-1][-1]
            HackIPUtility.output(system_data,hostname,ip_address,fqdn,private_ip_addr)

            
        except Exception as e:
            rprint(e)
            rprint('[red]error while getting IP address or invalid hostname!')
    
    def _linux(self,system_data):
        rprint("[yellow]---------------------------Linux---------------------------------")
        try :
            
            hostname = socket.gethostname() # returns hostname
            fqdn = socket.getfqdn('www.google.com') # returns fully qualified domain name for name
            ip_address = socket.gethostbyname(hostname)  # returns IPv4 address with respect to hostname
            os.system('ip addr > out.txt')
            f = open("out.txt", "r")
            strings = re.findall(r'192.168.\d{1,3}.\d{1,3}', f.read())
            private_ip_addr = strings[-2]
            HackIPUtility.output(system_data,hostname,ip_address,fqdn,private_ip_addr)

        except Exception as e:
            rprint(e)
            rprint('[red]error while getting IP address or invalid hostname!')
    
    def _macos(self,system_data):
        rprint("[yellow]---------------------------MacOS---------------------------------")
        try :
            hostname = socket.gethostname() # returns hostname
            fqdn = socket.getfqdn('www.google.com') # returns fully qualified domain name for name
            ip_address = socket.gethostbyname(hostname)  # returns IPv4 address with respect to hostname
            private_ip_addr = socket.gethostbyname_ex(hostname)[-1][-1]
            rprint(private_ip_addr)
            HackIPUtility.output(system_data,hostname,ip_address,fqdn,private_ip_addr)
            

        except Exception as e:
            rprint(e)
            rprint('[red]error while getting IP address or invalid hostname!')

    def _start(self,*args,**kwargs):

        rprint('''[green]
'##::::'##::::'###:::::'######::'##:::'##::::'####:'########::
 ##:::: ##:::'## ##:::'##... ##: ##::'##:::::. ##:: ##.... ##:
 ##:::: ##::'##:. ##:: ##:::..:: ##:'##::::::: ##:: ##:::: ##:
 #########:'##:::. ##: ##::::::: #####:::::::: ##:: ########::
 ##.... ##: #########: ##::::::: ##. ##::::::: ##:: ##.....:::
 ##:::: ##: ##.... ##: ##::: ##: ##:. ##:::::: ##:: ##::::::::
 ##:::: ##: ##:::: ##:. ######:: ##::. ##::::'####: ##::::::::
..:::::..::..:::::..:::......:::..::::..:::::....::..:::::::::
            ''')

        system_data = platform.uname()
        os_name = str(system_data.system)

        if os_name.lower()=="windows" :
            self._windows(system_data)
            
        elif os_name.lower() == 'linux':
            self._linux(system_data)

        elif os_name.lower() == 'darwin':
            self._macos(system_data)

        rprint("[yellow]"+"-"*20)