from enum import Enum
import netifaces


class CommonPort(Enum):
    FTP = (
        21,
        "FTP - Check for anonymous access, weak credentials, or outdated server versions.",
    )
    SSH = (
        22,
        "SSH - Ensure strong credentials and secure configurations; update to avoid vulnerabilities.",
    )
    TELNET = (
        23,
        "Telnet - Insecure protocol; consider replacing with SSH due to risk of data interception.",
    )
    SMTP = (
        25,
        "SMTP - Verify configurations to prevent open relay and secure against spam or abuse.",
    )
    DNS = (53, "DNS - Secure against DNS hijacking and ensure proper configuration.")
    HTTP = (
        80,
        "HTTP - Check for vulnerable web applications, outdated server software, and SSL/TLS misconfigurations.",
    )
    POP3 = (
        110,
        "POP3 - Ensure encrypted connections; consider security of email data in transit.",
    )
    IMAP = (
        143,
        "IMAP - Like POP3, ensure secure connections and email data protection.",
    )
    HTTPS = (
        443,
        "HTTPS - Regularly update SSL/TLS certificates and use strong encryption protocols.",
    )
    SMB = (
        445,
        "SMB - Secure against vulnerabilities like EternalBlue; regularly update and patch.",
    )
    MYSQL = (
        3306,
        "MySQL - Secure against SQL injection, unauthorized access, and ensure database encryption.",
    )
    RDP = (
        3389,
        "RDP - Protect against vulnerabilities like BlueKeep; use strong authentication and encryption.",
    )
    VNC = (5900, "VNC - Ensure secure, encrypted connections and use strong passwords.")
    HTTP_ALT = (
        8080,
        "HTTP-alt - Like port 80, check for web application vulnerabilities and secure configurations.",
    )
    HTTPS_ALT = (
        8443,
        "HTTPS-alt - As with standard HTTPS, use strong encryption and keep certificates updated.",
    )
    ELASTICSEARCH = (
        9200,
        "Elasticsearch - Secure against unauthorized access and data exfiltration risks.",
    )
    MONGODB = (
        27017,
        "MongoDB - Implement authentication, encryption, and protect against unauthorized access.",
    )

    def __init__(self, port, description):
        self.port = port
        self.description = description


def get_service_name(port):
    for service in CommonPort:
        if service.port == port:
            return f"{service.name} - {service.description}"
    return "Unknown"


def get_local_ip_addresses():
    ip_list = []
    for interface in netifaces.interfaces():
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            for link in addresses[netifaces.AF_INET]:
                ip_list.append(link["addr"])
    return ip_list
