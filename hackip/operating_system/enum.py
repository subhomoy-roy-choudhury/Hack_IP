from enum import Enum


class InformationParameter(Enum):
    SYSTEM = "system_information"
    CPU = "cpu_information"
    MEMORY = "memory_information"
    DISK = "disk_information"
    NETWORK = "network_information"
    PUBLIC_IP = "public_ip_details"