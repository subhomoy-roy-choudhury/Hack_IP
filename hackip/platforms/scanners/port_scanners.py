import socket
import logging
import threading
from queue import Queue

logger = logging.getLogger(__name__)


def scan_port(ip, port, open_ports):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex((ip, port)) == 0:
                open_ports.put(port)
    except Exception as e:
        print(f"Error scanning port {port}: {e}")


def find_open_ports(ip_addresses, port_range):
    open_ports = Queue()
    threads = []

    for ip in ip_addresses:
        for port in range(*port_range):
            thread = threading.Thread(target=scan_port, args=(ip, port, open_ports))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()

    # Extract ports from the queue and return them as a list
    return list(open_ports.queue)
