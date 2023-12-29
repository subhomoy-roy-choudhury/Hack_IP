import requests
import logging
from urllib.parse import quote
import psutil
from datetime import datetime
from helpers import get_size, encoding_result, get_shortened_url

logger = logging.getLogger(__name__)

def my_ip_location(dictionary):
    response = requests.get("https://ipinfo.io")
    response = response.json()

    # geolite database dict values and fine tunning
    ip = response["ip"]
    city = response["city"]
    region = response["region"]
    country = response["country"]
    location = response["loc"]
    network_provider = response["org"]
    postal_code = response["postal"]
    timezone = response["timezone"]

    print("Public IP address : {}".format(ip))
    dictionary["ip-address"] = ip
    print("City :-", city)
    dictionary["city"] = city
    print("Region :-", region)
    dictionary["region"] = region
    print("Country :-", country)
    dictionary["country"] = country
    print("Location :-", location)
    dictionary["location"] = location
    print("Network Provider :-", network_provider)
    dictionary["network_provider"] = network_provider
    print("Postal Code :-", postal_code)
    dictionary["postal_code"] = postal_code
    print("Timezone :-", timezone)
    dictionary["timezone"] = timezone

    return dictionary


def output(system_data, hostname, ip_address, fqdn, private_ip_addr):
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
    print(dictionary)
    encoded_str = encoding_result(dictionary)
    result_link = f"http://127.0.0.1:3000/?encoded_string={quote(encoded_str.decode())}"
    result_link = get_shortened_url(result_link)



def get_disk_informnation(dictionary={}):
    # Disk Information
    print("=" * 40, "Disk Information", "=" * 40)
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


def get_network_information():
    # Network information
    print("=" * 40, "Network Information", "=" * 40)
    # get all network interfaces (virtual and physical)
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            print(f"=== Interface: {interface_name} ===")
            if str(address.family) == "AddressFamily.AF_INET":
                print(f"  IP Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast IP: {address.broadcast}")
            elif str(address.family) == "AddressFamily.AF_PACKET":
                print(f"  MAC Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast MAC: {address.broadcast}")
    # get IO statistics since boot
    net_io = psutil.net_io_counters()
    print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
    print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")
