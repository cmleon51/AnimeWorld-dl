import os
from urllib.parse import urljoin,urlparse,urlunparse
import requests
from bs4 import BeautifulSoup as b4
import concurrent.futures
from api.episode import Episode

BASE_LINK = "https://www.animeworld.so"
MAX_CONCURRENT_DOWNLOADS = 10

def animew_download_episodes(anime_url,to="./"):
    anime_page = requests.get(anime_url)

    if anime_page.status_code != 200:
        print(f"could not reach url:{anime_url}")
        exit()

    soup_page = b4(anime_page.text,"html.parser")
    episodes_div = soup_page.find("div",class_="server active")
    episodes_lists = episodes_div.find_all("ul",class_="episodes")

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_CONCURRENT_DOWNLOADS) as executor:
        for ep_list in episodes_lists:
            episodes = ep_list.find_all("li",class_="episode")
            for episode in episodes:
                episode_url = urljoin(BASE_LINK,episode.find('a').get("href"))
                ep = Episode(episode_url)
                executor.submit(ep.write_to_file,to)
