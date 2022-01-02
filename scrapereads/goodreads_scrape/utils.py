from bs4 import BeautifulSoup
from urllib.request import urlopen
import socket
import time

def get_soup(link, tries=3, timeout=10, wait=3):
    for _ in range(tries):
        try:
            site = urlopen(link, timeout=timeout)
            soup = BeautifulSoup(site.read(), 'html.parser')
            break
        except socket.timeout:
            time.sleep(wait)
    return soup

def get_id_from_url(url):
    split_by = '.' if '.' in url else '-'
    return url.split(split_by)[0].split('/')[-1]