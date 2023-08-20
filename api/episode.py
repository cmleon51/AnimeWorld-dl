import os
from tqdm import tqdm
from urllib.parse import urljoin,urlparse,urlunparse
import requests
from bs4 import BeautifulSoup as b4

class Episode:
    def __init__(self,episode_url):
        #costants
        self._chunk_size = 1024 * 1024

        #defined here
        self.download_url = ""
        self.name = ""
        
        #defined in the download function
        self.size = None
        self.stream = None

        page_episode = requests.get(episode_url)
        soup_episode = b4(page_episode.text,"html.parser")

        download_page_url = soup_episode.find('a',id="downloadLink").get("href")
        response_head = requests.head(download_page_url)

        if response_head.status_code != 200:
            download_page_url = soup_episode.find('a',id="alternativeDownloadLink").get("href")

        parsed_url = urlparse(download_page_url)
        base_url = urlunparse((parsed_url.scheme, parsed_url.netloc, '', '', '', ''))

        page_download = requests.get(download_page_url)
        soup_download_page = b4(page_download.text,"html.parser")

        self.download_url = urljoin(
                base_url,
                soup_download_page.find('a',class_='btn btn-primary p-2', download=True).get("href"))
        self.name = os.path.basename(self.download_url)

    def download(self):
        response_head = requests.head(self.download_url)

        if response_head.status_code != 200:
            print("request to {self.download_url} didn't work")
            return False

        self.size = int(response_head.headers.get('content-length',0))
        self.stream = requests.get(self.download_url,stream=True)

        return True

    def write_to_file(self,to):
        if self.stream is None and self.size is None:
            if self.download() == False:
                return

        to = os.path.expanduser(to)
        download_path = os.path.join(to,self.name)

        if os.path.exists(download_path):
            print(f"anime episode {self.name} already exists")
            return

        with open(download_path,"wb") as file,tqdm(
                desc=download_path,total=self.size,unit='B',unit_scale=True,unit_divisor=self._chunk_size
                ) as pbar:
            for chunk in self.stream.iter_content(chunk_size=self._chunk_size):
                file.write(chunk)
                pbar.update(len(chunk))
