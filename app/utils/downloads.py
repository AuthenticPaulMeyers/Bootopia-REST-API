import os
import requests
from urllib.parse import urlparse

def is_localhost_url(url):
    return url.startswith("http://127.0.0.1") or url.startswith("http://localhost")

def get_local_path_from_url(url, static_folder='static'):
    parsed = urlparse(url)
    local_path = parsed.path  # /static/uploads/files/filename.pdf
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))  # root dir
    return os.path.join(base_dir, local_path.lstrip('/'))

def download_or_get_local_file(url, save_as="tmp/downloaded.pdf"):
    if is_localhost_url(url):
        local_path = get_local_path_from_url(url)
        if os.path.exists(local_path):
            return local_path
        else:
            raise FileNotFoundError(f"Local file not found: {local_path}")
    else:
        response = requests.get(url)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(save_as), exist_ok=True)
            with open(save_as, "wb") as f:
                f.write(response.content)
            return save_as
        else:
            raise Exception(f"Failed to download file. Status: {response.status_code}")
