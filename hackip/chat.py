import os
import logging

from .constants import GENERATED_REPORT_FOLDER_NAME, ASSISTANT_NAME, ASSISTANT_MODEL
from .assistant.utils import AssistantAPI

logger = logging.getLogger(__name__)

REPORT_FILE_PATH = os.path.join(GENERATED_REPORT_FOLDER_NAME, "overall-report.json")

CHAT_HISTORY = []


def get_initial_prompt():
    INITIAL_PROMPT = """
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

      active_processes:
        cpu_percent: Percentage of CPU usage by the process
        username: Username under which the process is running
        pid: Process ID (a unique identifier for each process)
        name: Name of the process (e.g., application name)
        memory_percent: Percentage of memory usage by the process
        status: Current status of the process (e.g., running, sleeping)

      network_open_ports:
        host: IP address of the host providing the service
        port: Network port on which the service is running
        state: Current state of the service (e.g., open, closed)
        name: General name of the service (e.g., http, ftp)
        product: Specific product name (e.g., software or framework running the service)
        version: Version of the product or service
        extrainfo: Additional information about the service, if available
        reason: Reason for the service state (e.g., syn-ack for open ports)
        conf: Confidence level in the service information (scale or value)
        service_name: Known or identified name of the service; "Unknown" if not identified

      Please write the response based on the schema
    """
    return INITIAL_PROMPT


def get_assistant_id(api, assistant_name):
    assistant_id = api.get_assistant_by_name(assistant_name)
    if assistant_id is None:
        assistant_id = api.create_assistant(
            name=assistant_name,
            instructions=get_initial_prompt(),
            model=ASSISTANT_MODEL,
            tools=[{"type": "retrieval"}],
            file_ids=[api.upload_file(REPORT_FILE_PATH).id],
        )
    return assistant_id


def generate_response(api_key, input_text):
    try:
        api = AssistantAPI()
        api.api_key = api_key
        assistant_id = get_assistant_id(api, ASSISTANT_NAME)

        thread_obj = api.create_thread()
        api.create_message(thread=thread_obj, content=input_text)
        initial_run_obj = api.create_run(
            thread_id=thread_obj.id, assistant_id=assistant_id
        )
        api.wait_on_run(run=initial_run_obj, thread=thread_obj)
        messages = api.get_thread_list(thread_id=thread_obj.id)
        return messages.data[0].content[0].text.value

    except Exception as e:
        logger.error(f"Error in generate_response: {str(e)}")
        return "[red]OpenAI text generation failed[/red]"
