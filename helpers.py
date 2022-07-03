import base64
import requests
import socket
from colorama import Fore, Back, Style , init
from urllib.parse import quote

class HackIPHelper(object):
    @staticmethod
    def encoding_result(dictionary):
        encoded_dict = str(dictionary).encode(encoding='UTF-8',errors='strict')
        base64_dict = base64.b64encode(encoded_dict)
        return base64_dict
    
    # Location Tracker
    @staticmethod
    def my_ip_location(dictionary):
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
        dictionary['ip-address'] = ip
        print("City :-",city)
        dictionary['city'] = city
        print("Region :-",region)
        dictionary['region'] = region
        print("Country :-",country)
        dictionary['country'] = country
        print("Location :-",location)
        dictionary['location'] = location
        print("Network Provider :-",network_provider)
        dictionary['network_provider'] = network_provider
        print("Postal Code :-",postal_code)
        dictionary['postal_code'] = postal_code
        print("Timezone :-",timezone)
        dictionary['timezone'] = timezone

        return dictionary
    
    @staticmethod
    def output(dictionary,system_data,hostname,ip_address,fqdn,private_ip_addr):
        print(Fore.GREEN + 'Operating System : '+str(system_data.system))
                    
        print('Machine : '+str(system_data.machine))
        dictionary['machine'] = system_data.machine
        print('Processor : '+str(system_data.processor))
        dictionary['processor'] = system_data.processor
        print('Release : '+str(system_data.release))
        dictionary['release'] = system_data.release
        print('Version : '+str(system_data.version))
        dictionary['version'] = system_data.version

        print(Fore.GREEN + f'Hostname : {hostname}')
        dictionary['hostname'] = system_data.version
        print('IP Address :', ip_address)
        print('FQDN', fqdn)
        print(socket.gethostbyname_ex(hostname)) # Return a triple (hostname, aliaslist, ipaddrlist)
        dictionary.update(HackIPHelper.my_ip_location(dictionary))
        print('Private IP Address : ', private_ip_addr)
        encoded_str = HackIPHelper.encoding_result(dictionary)
        result_link = f'http://127.0.0.1:3000/?encoded_string={quote(encoded_str.decode())}'
        print(result_link)