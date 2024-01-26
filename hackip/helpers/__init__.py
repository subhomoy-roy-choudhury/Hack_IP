import base64
import json
import logging
import os
import re

import requests

logger = logging.getLogger(__name__)


def get_shortened_url(url: str, api_key: str = None):
    shortened_url = url
    if api_key:
        # api_key = "b5a0e1bfd3c3521177a973b16ca39225b891e"
        api_url = f"https://cutt.ly/api/api.php?key={api_key}&short={url}"  # "https://cutt.ly/api/api.php?key={api_key}&short={url}&name=some_unique_name"
        data = requests.get(api_url).json()["url"]
        if data["status"] == 7:
            # OK, get shortened URL
            shortened_url = data["shortLink"]
            logger.info(f"Shortened URL: {shortened_url}")
        else:
            logger.critical(f"[!] Error Shortening URL: {data}")
    else:
        logger.warning("Cuttly API Token Not Found")

    return shortened_url


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
    """
    if bytes < 0:
        raise ValueError("Number of bytes cannot be negative")

    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z", "Y"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
    return f"{bytes:.2f}Y{suffix}"


def encoding_result(dictionary):
    encoded_dict = str(dictionary).encode(encoding="UTF-8", errors="strict")
    base64_dict = base64.b64encode(encoded_dict)
    return base64_dict


def slug_to_title(slug, seperator="_"):
    words = slug.split(seperator)  # Split the slug by hyphens
    title_cased_words = [word.capitalize() for word in words]  # Capitalize each word
    return " ".join(title_cased_words)  # Join the words with spaces


def write_json(filename, data):
    # Check if file doesn't exist and create it if necessary
    if not os.path.exists(filename):
        # Perform any specific action if the file does not exist
        logger.error(f"File {filename} does not exist. Creating new file.")
        open(filename, "w").close()  # Create the file

    # Writing JSON data
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def read_json(filename):
    # Reading the JSON data
    with open(filename, "r") as file:
        data = json.load(file)
    return data


# Function to get symbol for test case status
def get_status_symbol(status):
    if status == "pass":
        return "[green]:heavy_check_mark:"  # Green tick
    elif status == "fail":
        return "[red]:x:"  # Red cross


def create_folder(foldername):
    # Check for empty folder name
    if not foldername:
        raise ValueError("Folder name cannot be empty")

    # Check for invalid characters in folder name (adjust regex as needed)
    if re.search(r'[<>:"/\\|?*]', foldername):
        raise ValueError("Folder name contains invalid characters")

    # Check for overly long folder names
    if len(foldername) > 255:  # Adjust based on filesystem limits
        raise ValueError("Folder name is too long")

    # Construct the full path
    full_path = os.path.join(os.getcwd(), foldername)

    # Check if the folder already exists
    if os.path.exists(full_path):
        return

    # Try to create the folder, handle potential permission error
    try:
        os.makedirs(full_path)
    except PermissionError:
        raise PermissionError("Insufficient permissions to create the folder")


def file_exists(file_path):
    """Check if a file exists at the given file path.

    Args:
        file_path (str): The path of the file to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.exists(file_path)
