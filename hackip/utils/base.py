import requests
from urllib.parse import quote
import psutil
from datetime import datetime
from ..helpers import get_size, encoding_result, get_shortened_url
from rich import print as rprint

class HackIPUtility(object):
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
    def output(system_data,hostname,ip_address,fqdn,private_ip_addr):
        dictionary = {}
        # print(Fore.GREEN + 'Operating System : '+str(system_data.system))
                    
        # print('Machine : '+str(system_data.machine))
        # dictionary['machine'] = system_data.machine
        # print('Processor : '+str(system_data.processor))
        # dictionary['processor'] = system_data.processor
        # print('Release : '+str(system_data.release))
        # dictionary['release'] = system_data.release
        # print('Version : '+str(system_data.version))
        # dictionary['version'] = system_data.version

        # print(Fore.GREEN + f'Hostname : {hostname}')
        # dictionary['hostname'] = system_data.version
        # print('IP Address :', ip_address)
        # print('FQDN', fqdn)
        # print(socket.gethostbyname_ex(hostname)) # Return a triple (hostname, aliaslist, ipaddrlist)
        # dictionary.update(HackIPHelper.my_ip_location(dictionary))
        # print('Private IP Address : ', private_ip_addr)
        dictionary['system-information'] = HackIPUtility.get_system_info(system_data)
        dictionary['boot-time'] = HackIPUtility.get_boot_time()
        dictionary['cpu-information'] = HackIPUtility.get_cpu_information()
        dictionary['memory-usage'] = HackIPUtility.get_memory_information()
        print(dictionary)
        encoded_str = encoding_result(dictionary)
        result_link = f'http://127.0.0.1:3000/?encoded_string={quote(encoded_str.decode())}'
        result_link = get_shortened_url(result_link)

    @staticmethod
    def get_system_info(system_data,dictionary=dict()):
        print("="*40, "System Information", "="*40)
        print(f"System: {system_data.system}")
        dictionary['system'] = system_data.system
        print(f"Node Name: {system_data.node}")
        dictionary['node'] = system_data.node
        print(f"Release: {system_data.release}")
        dictionary['release'] = system_data.release
        print(f"Version: {system_data.version}")
        dictionary['version'] = system_data.version
        print(f"Machine: {system_data.machine}")
        dictionary['machine'] = system_data.machine
        print(f"Processor: {system_data.processor}")
        dictionary['processor'] = system_data.processor

        return dictionary
    
    @staticmethod
    def get_boot_time(dictionary=dict()):
        # Boot Time
        print("="*40, "Boot Time", "="*40)
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
        return f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"
    
    @staticmethod
    def get_cpu_information(dictionary=dict()):
        try :
            # let's print CPU information
            print("="*40, "CPU Info", "="*40)
            # number of cores
            print("Physical cores:", psutil.cpu_count(logical=False))
            dictionary['physical-cores'] = psutil.cpu_count(logical=False)
            print("Total cores:", psutil.cpu_count(logical=True))
            dictionary['total-cores'] = psutil.cpu_count(logical=True)
            # CPU frequencies
            cpufreq = psutil.cpu_freq()
            print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
            dictionary['maximum-frequency'] = f"{cpufreq.max:.2f}Mhz"
            print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
            dictionary['minimum-frequency'] = f"{cpufreq.min:.2f}Mhz"
            print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
            dictionary['current-frequency'] = f"{cpufreq.current:.2f}Mhz"
            # CPU usage
            print("CPU Usage Per Core:")
            for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
                print(f"Core {i}: {percentage}%")
                dictionary[f'core-{i}'] = f"{percentage}%"
            total_cpu_usage = psutil.cpu_percent()
            dictionary['total-cpu-usage'] = f"{total_cpu_usage}%"
            print(f"Total CPU Usage: {total_cpu_usage}%")
        
        except Exception as e:
            print(e)
        finally :
            return dictionary

    @staticmethod
    def get_memory_information(dictionary=dict()):
        # Memory Information
        print("="*40, "Memory Information", "="*40)
        # get the memory details
        svmem = psutil.virtual_memory()
        print(f"Total: {get_size(svmem.total)}")
        dictionary['total-space'] = get_size(svmem.total)
        print(f"Available: {get_size(svmem.available)}")
        dictionary['available-space'] = get_size(svmem.available)
        print(f"Used: {get_size(svmem.used)}")
        dictionary['used-space'] = get_size(svmem.used)
        print(f"Percentage: {svmem.percent}%")
        dictionary['percentage-space'] = get_size(svmem.percent)

        print("="*20, "SWAP", "="*20)
        # get the swap memory details (if exists)
        swap = psutil.swap_memory()
        swap_res_dict = dict()
        print(f"Total: {get_size(swap.total)}")
        swap_res_dict['total-space'] = get_size(swap.total)
        print(f"Free: {get_size(swap.free)}")
        swap_res_dict['free-space'] = get_size(swap.free)
        print(f"Used: {get_size(swap.used)}")
        swap_res_dict['used-space'] = get_size(swap.used)
        print(f"Percentage: {swap.percent}%")
        swap_res_dict['percentage-space'] = get_size(swap.percent)
        dictionary.update({'swap':swap_res_dict})

        return dictionary
    
    @staticmethod
    def get_disk_informnation(dictionary={}):
        # Disk Information
        print("="*40, "Disk Information", "="*40)
        print("Partitions and Usage:")
        # get all disk partitions
        partitions = psutil.disk_partitions()
        for partition in partitions:
            print(f"=== Device: {partition.device} ===")
            print(f"  Mountpoint: {partition.mountpoint}")
            print(f"  File system type: {partition.fstype}")
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                # this can be catched due to the disk that
                # isn't ready
                continue
            print(f"  Total Size: {get_size(partition_usage.total)}")
            print(f"  Used: {get_size(partition_usage.used)}")
            print(f"  Free: {get_size(partition_usage.free)}")
            print(f"  Percentage: {partition_usage.percent}%")
        # get IO statistics since boot
        disk_io = psutil.disk_io_counters()
        print(f"Total read: {get_size(disk_io.read_bytes)}")
        print(f"Total write: {get_size(disk_io.write_bytes)}")

    @staticmethod
    def get_network_information():
        # Network information
        print("="*40, "Network Information", "="*40)
        # get all network interfaces (virtual and physical)
        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                print(f"=== Interface: {interface_name} ===")
                if str(address.family) == 'AddressFamily.AF_INET':
                    print(f"  IP Address: {address.address}")
                    print(f"  Netmask: {address.netmask}")
                    print(f"  Broadcast IP: {address.broadcast}")
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    print(f"  MAC Address: {address.address}")
                    print(f"  Netmask: {address.netmask}")
                    print(f"  Broadcast MAC: {address.broadcast}")
        # get IO statistics since boot
        net_io = psutil.net_io_counters()
        print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
        print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")