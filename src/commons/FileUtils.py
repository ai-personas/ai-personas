import requests
from pathlib import Path
from urllib.parse import urlparse

class FileUtils:

    def __init__(self, target_folder=''):
        self.target_folder = target_folder
        Path(target_folder).mkdir(parents=True, exist_ok=True)

    def downloadDataToLocal(self, url):
        if url is None or not self.is_url_valid(url):
            return None
        local_filename = self.target_folder + url.split('/')[-1]
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename

    def is_url_valid(self, url):
        try:
            result = urlparse(url)
            if result.scheme in (None, '') or result.netloc in (None, ''):
                return False
        except:
            return False
        return True

    def getTargetFolder(self):
        return self.target_folder
