import logging
import os
import platform
import socket
from collections import defaultdict
from datetime import datetime
from urllib.parse import quote

import psutil
import requests
from ..constants import BASE_WEB_URL, GENERATED_REPORT_FOLDER_NAME
from ..helpers import (
    encoding_result,
    get_shortened_url,
    get_size,
    slug_to_title,
    write_json,
)
from .scanners.helpers import get_local_ip_addresses, get_service_name
from .scanners.nmap_port_scanner import (
    find_open_ports as find_open_ports_advanced,
)
from .scanners.port_scanners import find_open_ports as find_open_ports_basic
from .utilities.decorators import fetch_info_wrapper
from .utilities.enum import InformationParameter
from rich.console import Console
from rich.panel import Panel
from rich.status import Status
from rich import print as rprint

logger = logging.getLogger(__name__)
console = Console()


class BaseOperatingSystem(object):
    def __init__(self, cuttly_api_key, advanced_scanning=False) -> None:
        self.os_name = None
        self.system_data = platform.uname()
        self.hostname = socket.gethostname()  # returns hostname
        self.private_ip_addr = None
        self.cuttly_api_key = cuttly_api_key
        self.advanced_scanning = advanced_scanning

    def _fetch_data_safely(self, fetch_function, error_message):
        try:
            return fetch_function()
        except Exception as e:
            logger.error(f"{error_message}: {e}")
            return {}

    @fetch_info_wrapper(
        fetch_info_name=slug_to_title(InformationParameter.SYSTEM.value)
    )
    def _format_system_info(self):
        return {
            "system": self.system_data.system,
            "node": self.system_data.node,
            "release": self.system_data.release,
            "version": self.system_data.version,
            "machine": self.system_data.machine,
            "processor": self.system_data.processor,
            "fqdn": socket.getfqdn(
                "www.google.com"
            ),  # returns fully qualified domain name for name
            "private-ip-address": self._get_private_ip_address(),
        }

    def _format_boot_time(self):
        # Boot Time
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        return f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"

    def _get_cpu_cores(self):
        result = {}
        try:
            result["physical-cores"] = psutil.cpu_count(logical=False)
            result["total-cores"] = psutil.cpu_count(logical=True)
        except Exception as e:
            logger.error(f"Error Fetching CPU cores data: {e}")
        return result

    def _get_cpu_freq(self):
        result = {}
        try:
            cpufreq = psutil.cpu_freq()
            result["maximum-frequency"] = f"{cpufreq.max:.2f}Mhz"
            result["minimum-frequency"] = f"{cpufreq.min:.2f}Mhz"
            result["current-frequency"] = f"{cpufreq.current:.2f}Mhz"
        except Exception as e:
            logger.error(f"Error Fetching CPU frequency data: {e}")
        return result

    def _get_cpu_usage_per_core(self):
        result = {}
        try:
            for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
                result[f"core-{i}"] = f"{percentage}%"
            total_cpu_usage = psutil.cpu_percent()
            result["total-cpu-usage"] = f"{total_cpu_usage}%"
        except Exception as e:
            logger.error(f"Error Fetching CPU Usage per core data: {e}")
        return result

    @fetch_info_wrapper(fetch_info_name=slug_to_title(InformationParameter.CPU.value))
    def _format_cpu_information(self):
        return {
            **self._fetch_data_safely(
                self._get_cpu_cores, "Error Fetching CPU cores data"
            ),
            **self._fetch_data_safely(
                self._get_cpu_freq, "Error Fetching CPU frequency data"
            ),
            **self._fetch_data_safely(
                self._get_cpu_usage_per_core, "Error Fetching CPU Usage per core data"
            ),
        }

    def _get_virtual_memory_information(self):
        result = {}
        try:
            svmem = psutil.virtual_memory()
            result["virtual-total-space"] = get_size(svmem.total)
            result["virtual-available-space"] = get_size(svmem.available)
            result["virtual-used-space"] = get_size(svmem.used)
            result["virtual-percentage-space"] = get_size(svmem.percent)
        except Exception as e:
            logger.error("Error Fetching Virtual Memory Information")
        return result

    def _get_swap_memory_information(self):
        result = {}
        try:
            swap = psutil.swap_memory()
            result["swap-total-space"] = get_size(swap.total)
            result["swap-free-space"] = get_size(swap.free)
            result["swap-used-space"] = get_size(swap.used)
            result["swap-percentage-space"] = get_size(swap.percent)
        except Exception as e:
            logger.error("Error Fetching Swap Memory Information")
        return result

    @fetch_info_wrapper(
        fetch_info_name=slug_to_title(InformationParameter.MEMORY.value)
    )
    def _format_memory_information(self):
        return {
            **self._get_virtual_memory_information(),
            **self._get_swap_memory_information(),
        }

    def _get_all_disk_partitions(self):
        result = {}
        partitions = self._fetch_data_safely(
            psutil.disk_partitions, "Error fetching all disk partitions data"
        )
        for partition in partitions:
            partition_info = self._get_partition_info(partition)
            if partition_info:
                result[partition.device] = partition_info
        return result

    def _get_partition_info(self, partition):
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            return {
                "mountpoint": partition.mountpoint,
                "file-system-type": partition.fstype,
                "total-size": get_size(partition_usage.total),
                "used-size": get_size(partition_usage.used),
                "free-size": get_size(partition_usage.free),
                "percentage": f"{partition_usage.percent}%",
            }
        except PermissionError as e:
            logger.warning(
                f"Insuffiecient Permission to access the file system {partition.device}"
            )
            return None

    @fetch_info_wrapper(fetch_info_name=slug_to_title(InformationParameter.DISK.value))
    def _format_disk_information(self):
        try:
            # get IO statistics since boot
            disk_io = psutil.disk_io_counters()
            return {
                "total-read": get_size(disk_io.read_bytes),
                "total-write": get_size(disk_io.write_bytes),
                **self._get_all_disk_partitions(),
            }
        except Exception as e:
            logger.error("Error fetching disk information")

    def _get_all_network_interfaces(self):
        result = defaultdict(dict)
        try:
            if_addrs = psutil.net_if_addrs()
            for interface_name, interface_addresses in if_addrs.items():
                for address in interface_addresses:
                    if address.family == socket.AF_INET:
                        address_key = "inet"
                    elif address.family == socket.AF_PACKET:
                        address_key = "packet"
                    else:
                        continue  # Skip if the address family is not of interest

                    result[interface_name][f"{address_key}-address"] = address.address
                    result[interface_name][f"{address_key}-netmask"] = address.netmask
                    result[interface_name][
                        f"{address_key}-broadcast"
                    ] = address.broadcast

        except Exception as e:
            logger.error(f"Error fetching network interface data: {e}")
        return dict(result)  # Convert back to regular dict for return

    def _get_private_ip_address(self):
        raise Exception("Not Implemented")

    @fetch_info_wrapper(
        fetch_info_name=slug_to_title(InformationParameter.NETWORK.value)
    )
    def _format_network_information(self):
        try:
            # get IO statistics since boot
            net_io = psutil.net_io_counters()
            return {
                "total-bytes-sent": get_size(net_io.bytes_sent),
                "total-bytes-recieved": get_size(net_io.bytes_recv),
                **self._get_all_network_interfaces(),
            }
        except Exception as e:
            logger.error(f"Error fetching network information : {e}")

    def _get_public_ip_information(self):
        response = requests.get("https://ipinfo.io")
        response = response.json()
        return response

    @fetch_info_wrapper(
        fetch_info_name=slug_to_title(InformationParameter.PUBLIC_IP.value)
    )
    def _format_public_ip_details(self):
        public_ip_info = self._get_public_ip_information()
        return {
            "public-ip-address": public_ip_info["ip"],
            "city": public_ip_info["city"],
            "region": public_ip_info["region"],
            "country": public_ip_info["country"],
            "location": public_ip_info["loc"],
            "network_provider": public_ip_info["org"],
            "postal_code": public_ip_info["postal"],
            "timezone": public_ip_info["timezone"],
        }

    @fetch_info_wrapper(
        fetch_info_name=slug_to_title(InformationParameter.ACTIVE_PROCESSES.value)
    )
    def _format_active_processes(self):
        # List all the processes running on the system with their details
        processes = []
        for proc in psutil.process_iter(
            ["pid", "name", "username", "cpu_percent", "memory_percent", "status"]
        ):
            try:
                # Get process detail as dictionary
                process_info = proc.info
                processes.append(process_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        # Sorting the processes based on memory and CPU usage and handling None values
        top_processes = sorted(
            processes,
            key=lambda x: (
                (x["memory_percent"] is not None, x["memory_percent"]),
                (x["cpu_percent"] is not None, x["cpu_percent"]),
            ),
            reverse=True,
        )[:20]
        return top_processes

    @fetch_info_wrapper(
        fetch_info_name=slug_to_title(InformationParameter.NETWORK_OPEN_PORTS.value)
    )
    def _format_open_ports(self) -> list:
        target_ips = get_local_ip_addresses()
        port_range = (20, 10255)

        # Choose the appropriate scanning function
        scan_func = (
            find_open_ports_advanced
            if self.advanced_scanning
            else find_open_ports_basic
        )

        open_ports = scan_func(target_ips, port_range)
        if self.advanced_scanning:
            return list(
                map(
                    lambda details: dict(
                        **details, service_name=get_service_name(details["port"])
                    ),
                    open_ports,
                )
            )
        else:
            return list(
                map(
                    lambda port: dict(port=port, service_name=get_service_name(port)),
                    open_ports,
                )
            )

    def prepare(self):
        method_mapping = {
            InformationParameter.SYSTEM: self._format_system_info,
            InformationParameter.CPU: self._format_cpu_information,
            InformationParameter.MEMORY: self._format_memory_information,
            InformationParameter.DISK: self._format_disk_information,
            InformationParameter.NETWORK: self._format_network_information,
            InformationParameter.PUBLIC_IP: self._format_public_ip_details,
            InformationParameter.ACTIVE_PROCESSES: self._format_active_processes,
            InformationParameter.NETWORK_OPEN_PORTS: self._format_open_ports,
        }

        result = {}
        with Status("[bold green]Fetching Information...", spinner="dots"):
            for info_param, method in method_mapping.items():
                formatted_info = method()
                if info_param == InformationParameter.SYSTEM:
                    formatted_info["boot_time"] = self._format_boot_time()
                result[info_param.value] = formatted_info

        return result

    def _create_webpage_link(self, data):
        encoded_str = encoding_result(data)
        result_link = f"{BASE_WEB_URL}/?encoded_string={quote(encoded_str.decode())}"
        result_link = get_shortened_url(result_link, self.cuttly_api_key)
        return result_link

    def _generate_report(self, data):
        try:
            report_filepath = os.path.join(
                os.getcwd(), GENERATED_REPORT_FOLDER_NAME, "overall-report.json"
            )
            write_json(report_filepath, data)
            console.print(
                "\n[+] Successfully generated system report \n",
                style="bold bright_blue",
            )
            rprint("[purple]Report File Path :[/purple]", end=" ")
            rprint(f"[blue]{report_filepath}[/blue] \n")
        except Exception as e:
            raise ValueError("Error Generating Report")

    def stdout(self):
        # Section divider with Title
        console.print(
            Panel(
                "System Report",
                expand=False,
                style="bright_yellow",
                border_style="bold",
            )
        )

        data = self.prepare()
        self._generate_report(data)
