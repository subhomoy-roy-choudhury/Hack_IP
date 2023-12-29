import platform
import psutil
import logging
from datetime import datetime
from rich import print as rprint
from helpers import get_size, slug_to_title

logger = logging.getLogger(__name__)


class BaseOperatingSystemUtils(object):
    def __init__(self) -> None:
        self.os_name = None
        self.system_data = platform.uname()

    def _format_system_info(self):
        return {
            "system": self.system_data.system,
            "node": self.system_data.node,
            "release": self.system_data.release,
            "version": self.system_data.version,
            "machine": self.system_data.machine,
            "processor": self.system_data.processor,
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

    def _format_memory_information(self):
        return {
            **self._get_virtual_memory_information(),
            **self._get_swap_memory_information(),
        }
    
    def _get_all_disk_partitions(self):
        result = {}
        try :
            partitions = psutil.disk_partitions()
            for partition in partitions:
                pass 
        except Exception as e:
            logger.error("Error fetching all disk partitions data")
        return result
    
    def _format_disk_information(self):
        pass

    def prepare(self):
        raise Exception("Not Implemented")

    def _output(self, data):
        try:
            for header, metadata in data.items():
                print("=" * 40, header, "=" * 40)
                for parameter, data in metadata.items():
                    rprint(f"{slug_to_title(parameter)}: {data}")
        except Exception as e:
            raise ValueError("Output Formatting Error")

    def stdout(self):
        rprint(
            f"[yellow]--------------------------- {self.os_name} ---------------------------------"
        )
        data = self.prepare()
        self._output(data)

        rprint("[yellow]" + "-" * 40)
