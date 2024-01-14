import nmap
import threading
from queue import Queue


def scan_open_ports(ip, queue):
    nm = nmap.PortScanner()
    nm.scan(ip, arguments="-sV")
    open_ports = []

    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            for port in nm[host][proto].keys():
                port_info = {
                    "host": host,
                    "port": port,
                    "state": nm[host][proto][port]["state"],
                    "name": nm[host][proto][port]["name"],
                    "product": nm[host][proto][port].get("product", ""),
                    "version": nm[host][proto][port].get("version", ""),
                    "extrainfo": nm[host][proto][port].get("extrainfo", ""),
                    "reason": nm[host][proto][port]["reason"],
                    "conf": nm[host][proto][port]["conf"],
                }
                open_ports.append(port_info)

    queue.put(open_ports)


def find_open_ports(ip_addresses, *args, **kwargs):
    threads = []
    queue = Queue()

    for ip in ip_addresses:
        t = threading.Thread(target=scan_open_ports, args=(ip, queue))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    all_open_ports = []
    while not queue.empty():
        all_open_ports.extend(queue.get())

    return all_open_ports
