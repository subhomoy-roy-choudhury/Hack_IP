import socket 
import os
import sys
import re
from colorama import Fore, Back, Style , init
from termcolor import colored
import platform
import psutil
# from pyfiglet import Figlet
import requests

init()

# '''
# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL
# '''
# f = Figlet(font='banner3-D') # banner3-D , standard , isometric2
# print('\n')
# print(colored(f.renderText(f'Hack IP'), 'green'))

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

# Location Tracker
def my_ip_location():
    response = requests.get('https://ipinfo.io')
    response = response.json()

    #geolite database dict values and fine tunning
    ip= response['ip']
    city=response['city']
    region = response['region']
    country=response['country']
    location = response['loc']
    network_provider=response['org']
    postal_code=response['postal']
    timezone=response['timezone']
    
    print('Public IP address : {}'.format(ip))
    print("City :-",city)
    print("Region :-",region)
    print("Country :-",country)
    print("Location :-",location)
    print("Network Provider :-",network_provider)
    print("Postal Code :-",postal_code)
    print("Timezone :-",timezone)

while True :

    system_data = platform.uname()
    os_name = str(system_data.system)
    print(Fore.BLUE + "Tell me your Operating System i.e. Windows,Linux,MacOS")
    print(Fore.CYAN + "[1] Windows")
    print(Fore.CYAN + "[2] Linux")
    print(Fore.CYAN + "[3] MacOS")
    print(Fore.CYAN + "[4] EXIT")
    print(Style.RESET_ALL)

    os_raw = input("Enter the choice :- ")
    os_int = int(os_raw)

    if os_int == 1 :

        if os_name.lower()=="windows" :

            print(Fore.YELLOW + "---------------------------Windows-------------------------------")
            try:

                hostname = socket.gethostname() # returns hostname
                ip_address = socket.gethostbyname(hostname)  # returns IPv4 address with respect to hostname
                fqdn = socket.getfqdn('www.google.com') # returns fully qualified domain name for name
                print(Fore.GREEN + 'Operating System : '+str(system_data.system))
                
                print('Machine : '+str(system_data.machine))
                print('Processor : '+str(system_data.processor))
                print('Release : '+str(system_data.release))
                print('Version : '+str(system_data.version))

                print(Fore.GREEN + f'Hostname : {hostname}')
                print('IP Address :', ip_address)
                print('FQDN', fqdn)
                print(socket.gethostbyname_ex(hostname)) # Return a triple (hostname, aliaslist, ipaddrlist)
                my_ip_location()
                print('Private IP Address : ', socket.gethostbyname_ex(hostname)[-1][-1])
                
            except Exception as e:
                print(e)
                print(Fore.RED + 'error while getting IP address or invalid hostname!')

        else:
            print(Fore.RED + "No Windows Installation Detected")
        print(Style.RESET_ALL)
        
    elif os_int == 2 :
        
        if os_name.lower() == 'linux':

            print(Fore.YELLOW + "---------------------------Linux---------------------------------")
            try :
                
                hostname = socket.gethostname() # returns hostname
                fqdn = socket.getfqdn('www.google.com') # returns fully qualified domain name for name
                ip_address = socket.gethostbyname(hostname)  # returns IPv4 address with respect to hostname
                os.system('ip addr > out.txt')
                f = open("out.txt", "r")
                strings = re.findall(r'192.168.\d{1,3}.\d{1,3}', f.read())

                print(Fore.GREEN + 'Operating System : '+str(system_data.system))
                print('Machine : '+str(system_data.machine))
                print('Processor : '+str(system_data.processor))
                print('Release : '+str(system_data.release))
                print('Version : '+str(system_data.version))

                print(f'Hostname : {hostname}')
                print('IP Address :', ip_address)
                print('FQDN', fqdn)
                print(socket.gethostbyname_ex(hostname)) # Return a triple (hostname, aliaslist, ipaddrlist)
                my_ip_location()
                print(f'Private IP Address : {strings[-2]}')

            except Exception as e:
                print(e)
                print(Fore.RED + 'error while getting IP address or invalid hostname!')
        
        else :
            print(Fore.RED + "No Linux Installation Detected")
        print(Style.RESET_ALL)

    elif os_int == 3 :

        if os_name.lower() == 'darwin':

            print(Fore.YELLOW + "---------------------------MacOS---------------------------------")
            try :
                
                hostname = socket.gethostname() # returns hostname
                fqdn = socket.getfqdn('www.google.com') # returns fully qualified domain name for name
                ip_address = socket.gethostbyname(hostname)  # returns IPv4 address with respect to hostname
                os.system('ip addr > out.txt')
                f = open("out.txt", "r")
                strings = re.findall(r'192.168.\d{1,3}.\d{1,3}', f.read())

                print(Fore.GREEN + 'Operating System : '+str(system_data.system))
                print('Machine : '+str(system_data.machine))
                print('Processor : '+str(system_data.processor))
                print('Release : '+str(system_data.release))
                print('Version : '+str(system_data.version))

                print(f'Hostname : {hostname}')
                print('IP Address :', ip_address)
                print('FQDN', fqdn)
                print(socket.gethostbyname_ex(hostname)) # Return a triple (hostname, aliaslist, ipaddrlist)
                my_ip_location()
                print(f'Private IP Address : {strings[-2]}')

            except Exception as e:
                print(e)
                print(Fore.RED + 'error while getting IP address or invalid hostname!')
        
        else :
            print(Fore.RED + "No MacOS Installation Detected")

        print(Style.RESET_ALL)

    elif os_int == 4 :

        print(Fore.YELLOW + "---------------------------EXIT----------------------------------")
        print(Style.RESET_ALL)
        sys.exit()

    print(Fore.YELLOW + "-----------------------------------------------------------------")

    arg = input("Do you want to continue (Y/N) : ")
    arg = str(arg)
    arg = arg.lower()
    if arg == 'y' :
        continue
    else :
        sys.exit()           