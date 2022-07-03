import socket
import os
import sys
import re
from colorama import Fore, Back, Style , init
import platform
# from pyfiglet import Figlet
from helpers import HackIPHelper

class HackTP(object):
    def __init__(self) -> None:
        init()
        print(Fore.GREEN +'''
'##::::'##::::'###:::::'######::'##:::'##::::'####:'########::
 ##:::: ##:::'## ##:::'##... ##: ##::'##:::::. ##:: ##.... ##:
 ##:::: ##::'##:. ##:: ##:::..:: ##:'##::::::: ##:: ##:::: ##:
 #########:'##:::. ##: ##::::::: #####:::::::: ##:: ########::
 ##.... ##: #########: ##::::::: ##. ##::::::: ##:: ##.....:::
 ##:::: ##: ##.... ##: ##::: ##: ##:. ##:::::: ##:: ##::::::::
 ##:::: ##: ##:::: ##:. ######:: ##::. ##::::'####: ##::::::::
..:::::..::..:::::..:::......:::..::::..:::::....::..:::::::::
            ''')

        self.run()
    
    def _windows(self,system_data,result_dict):
        print(Fore.YELLOW + "---------------------------Windows-------------------------------")
        try:

            hostname = socket.gethostname() # returns hostname
            ip_address = socket.gethostbyname(hostname)  # returns IPv4 address with respect to hostname
            fqdn = socket.getfqdn('www.google.com') # returns fully qualified domain name for name
            private_ip_addr = socket.gethostbyname_ex(hostname)[-1][-1]
            result_dict = HackIPHelper.output(result_dict,system_data,hostname,ip_address,fqdn,private_ip_addr)

            
        except Exception as e:
            print(e)
            print(Fore.RED + 'error while getting IP address or invalid hostname!')
        
        print(Style.RESET_ALL)
    
    def _linux(self,system_data,result_dict):
        print(Fore.YELLOW + "---------------------------Linux---------------------------------")
        try :
            
            hostname = socket.gethostname() # returns hostname
            fqdn = socket.getfqdn('www.google.com') # returns fully qualified domain name for name
            ip_address = socket.gethostbyname(hostname)  # returns IPv4 address with respect to hostname
            os.system('ip addr > out.txt')
            f = open("out.txt", "r")
            strings = re.findall(r'192.168.\d{1,3}.\d{1,3}', f.read())
            private_ip_addr = strings[-2]
            result_dict = HackIPHelper.output(result_dict,system_data,hostname,ip_address,fqdn,private_ip_addr)

        except Exception as e:
            print(e)
            print(Fore.RED + 'error while getting IP address or invalid hostname!')
        
        print(Style.RESET_ALL)
    
    def _macos(self,system_data,result_dict):
        print(Fore.YELLOW + "---------------------------MacOS---------------------------------")
        try :
            hostname = socket.gethostname() # returns hostname
            fqdn = socket.getfqdn('www.google.com') # returns fully qualified domain name for name
            ip_address = socket.gethostbyname(hostname)  # returns IPv4 address with respect to hostname
            os.system('ip addr > out.txt')
            f = open("out.txt", "r")
            strings = re.findall(r'192.168.\d{1,3}.\d{1,3}', f.read())
            private_ip_addr = strings[-2]
            result_dict = HackIPHelper.output(result_dict,system_data,hostname,ip_address,fqdn,private_ip_addr)
            

        except Exception as e:
            print(e)
            print(Fore.RED + 'error while getting IP address or invalid hostname!')

        print(Style.RESET_ALL)

    def run(self):

        while True :

            system_data = platform.uname()
            os_name = str(system_data.system)
        
            result_dict = dict()

            if os_name.lower()=="windows" :
                self._windows(system_data,result_dict)
                
            elif os_name.lower() == 'linux':
                self._linux(system_data,result_dict)

            elif os_name.lower() == 'darwin':
                self._macos(system_data,result_dict)

            print(Fore.YELLOW + "-----------------------------------------------------------------")

            arg = input("Do you want to continue (Y/N) : ")
            arg = str(arg)
            arg = arg.lower()
            if arg == 'y' :
                continue
            else :
                sys.exit()           

if __name__ == '__main__':
    HackTP()