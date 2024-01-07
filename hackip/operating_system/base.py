import os
import platform
import psutil
import socket
import logging
import requests
from urllib.parse import quote
from datetime import datetime

from rich.console import Console
from rich.status import Status
from rich.panel import Panel

from hackip.helpers import (
    get_size,
    encoding_result,
    get_shortened_url,
    write_json,
    slug_to_title,
)
from hackip.operating_system.enum import InformationParameter
from hackip.operating_system.decorators import fetch_info_wrapper
from hackip.constants import BASE_WEB_URL, GENERATED_REPORT_FOLDER_NAME

logger = logging.getLogger(__name__)
console = Console()


class BaseOperatingSystemUtils(object):
    def __init__(self) -> None:
        self.os_name = None
        self.system_data = platform.uname()
        self.hostname = socket.gethostname()  # returns hostname
        self.private_ip_addr = None

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
            **self._get_cpu_cores(),
            **self._get_cpu_freq(),
            **self._get_cpu_usage_per_core(),
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
        try:
            partitions = psutil.disk_partitions()
            for partition in partitions:
                result[partition.device] = {
                    "mountpoint": partition.mountpoint,
                    "file-system-type": partition.fstype,
                }
                try:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                    result[partition.device]["total-size"] = get_size(
                        partition_usage.total
                    )
                    result[partition.device]["used-size"] = get_size(
                        partition_usage.used
                    )
                    result[partition.device]["free-size"] = get_size(
                        partition_usage.free
                    )
                    result[partition.device][
                        "percentage"
                    ] = f"{partition_usage.percent}%"
                except PermissionError as e:
                    logger.warning(
                        f"Insuffiecient Permission to access the file system {partition.device}"
                    )
        except Exception as e:
            logger.error("Error fetching all disk partitions data")
        return result

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
        result = {}
        try:
            if_addrs = psutil.net_if_addrs()
            for interface_name, interface_addresses in if_addrs.items():
                if interface_name not in result:
                    result[interface_name] = {}
                for address in interface_addresses:
                    if address.family == socket.AF_INET:
                        result[interface_name].update(
                            {
                                "ip-address": address.address,
                                "netmask": address.netmask,
                                "broadcast-ip": address.broadcast,
                            }
                        )
                    elif address.family == socket.AF_PACKET:
                        result[interface_name].update(
                            {
                                "mac-address": address.address,
                                "netmask": address.netmask,
                                "broadcast-mac": address.broadcast,
                            }
                        )
        except Exception as e:
            logger.error("Error fetching all network interface data: %s", str(e))
        return result

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

    def prepare(self):
        result = {}
        with Status("[bold green]Fetching Informstion...", spinner="dots") as status:
            result[InformationParameter.SYSTEM.value] = {
                **self._format_system_info(),
                "boot_time": self._format_boot_time(),
            }
            result[InformationParameter.CPU.value] = self._format_cpu_information()
            result[
                InformationParameter.MEMORY.value
            ] = self._format_memory_information()
            result[InformationParameter.DISK.value] = self._format_disk_information()
            result[
                InformationParameter.NETWORK.value
            ] = self._format_network_information()
            result[
                InformationParameter.PUBLIC_IP.value
            ] = self._format_public_ip_details()
            return result

    def _create_webpage_link(self, data):
        encoded_str = encoding_result(data)
        result_link = f"{BASE_WEB_URL}/?encoded_string={quote(encoded_str.decode())}"
        result_link = get_shortened_url(result_link)
        return result_link

    def _generate_report(self, data):
        try:
            write_json(
                os.path.join(GENERATED_REPORT_FOLDER_NAME, "overall-report.json"), data
            )
            console.print(
                "\n[+] Successfully generated system report", style="bold bright_blue"
            )
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
