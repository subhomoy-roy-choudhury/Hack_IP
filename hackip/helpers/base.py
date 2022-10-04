import base64
import requests

def get_shortened_url(url):

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
        print("Shortened URL:", shortened_url)
    else:
        print("[!] Error Shortening URL:", data)
    
    return shortened_url

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def encoding_result(dictionary):
    encoded_dict = str(dictionary).encode(encoding='UTF-8',errors='strict')
    base64_dict = base64.b64encode(encoded_dict)
    return base64_dict