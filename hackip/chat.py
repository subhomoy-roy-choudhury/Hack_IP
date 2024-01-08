import os
from openai import OpenAI

from hackip.utils import load_configuration
from hackip.helpers import read_json
from hackip.constants import GENERATED_REPORT_FOLDER_NAME

# OpenAI Client
client = OpenAI(api_key=load_configuration()["credentials"]["openai_key"])

REPORT_FILE_PATH = os.path.join(GENERATED_REPORT_FOLDER_NAME, "overall-report.json")

INITIAL_PROMPT = f"""
You are a cyber security expert. 
You are supplied with the system as well as network details. 

The schema and details of the data is given below :- \n\n

system_information:
  system: Operating system name (e.g., Darwin, Windows, Linux)
  node: System's network name (e.g., hostname)
  release: OS release version
  version: Detailed OS version and build information
  machine: Architecture of the system (e.g., x86_64, arm64)
  processor: Processor type (e.g., x86, arm)
  fqdn: Fully Qualified Domain Name of the system
  private-ip-address: Private IP address of the system
  boot_time: Time when the system was last booted

cpu_information:
  physical-cores: Number of physical CPU cores
  total-cores: Total number of CPU cores (including virtual cores if any)
  core-0 to core-7: CPU usage percentage for each core
  total-cpu-usage: Total CPU usage percentage

memory_information:
  virtual-total-space: Total virtual memory available
  virtual-available-space: Available virtual memory
  virtual-used-space: Used virtual memory
  virtual-percentage-space: Percentage of virtual memory used
  swap-total-space: Total swap memory available
  swap-free-space: Available swap memory
  swap-used-space: Used swap memory
  swap-percentage-space: Percentage of swap memory used

disk_information:
  total-read: Total data read from disk
  total-write: Total data written to disk
  Each disk device (e.g., /dev/disk3s1s1):
    mountpoint: Mount point of the disk
    file-system-type: File system type (e.g., apfs, ntfs)
    total-size: Total size of the disk partition
    used-size: Used space on the disk partition
    free-size: Free space available on the disk partition
    percentage: Percentage of disk space used

network_information:
  total-bytes-sent: Total bytes sent over the network
  total-bytes-recieved: Total bytes received over the network
  Each network interface (e.g., lo0):
    ip-address: IP address assigned to the interface
    netmask: Network mask
    broadcast-ip: Broadcast IP address (if applicable)

public_ip_details:
  public-ip-address: Public IP address of the system
  city: City based on the public IP address
  region: Region or state based on the public IP address
  country: Country based on the public IP address
  location: Geographical location (latitude, longitude)
  network_provider: Internet service provider or network provider
  postal_code: Postal code based on the public IP address
  timezone: Timezone based on the public IP address

\n\n The system details is given below :- \n\n ${read_json(REPORT_FILE_PATH)} \n

Please write the response based on the schema 
"""

CHAT_HISTORY = [{"role": "system", "content": INITIAL_PROMPT}]


def generate_response(input):
    CHAT_HISTORY.append({"role": "user", "content": input})
    assistant_response = get_completion(CHAT_HISTORY)
    CHAT_HISTORY.append({"role": "assistant", "content": assistant_response})
    return assistant_response


def get_completion(messages, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.9,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message.content