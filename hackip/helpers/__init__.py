import base64
import requests
import logging

logger = logging.getLogger(__name__)


def get_shortened_url(url):
    shortened_url = None
    api_key = "b5a0e1bfd3c3521177a973b16ca39225b891e"
    # preferred name in the URL
    api_url = f"https://cutt.ly/api/api.php?key={api_key}&short={url}"
    # or
    # api_url = f"https://cutt.ly/api/api.php?key={api_key}&short={url}&name=some_unique_name"
    # make the request
    data = requests.get(api_url).json()["url"]
    if data["status"] == 7:
        # OK, get shortened URL
        shortened_url = data["shortLink"]
        logger.info(f"Shortened URL: {shortened_url}")
    else:
        logger.critical(f"[!] Error Shortening URL: {data}")

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


def slug_to_title(slug):
    words = slug.split("-")  # Split the slug by hyphens
    title_cased_words = [word.capitalize() for word in words]  # Capitalize each word
    return " ".join(title_cased_words)  # Join the words with spaces
