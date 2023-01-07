from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import socket
import time
from scrapereads.configs import headers
import chardet

def get_soup(link, tries=3, timeout=10, wait=3):
    """

    Parameters
    ----------
    link :
        
    tries :
         (Default value = 3)
    timeout :
         (Default value = 10)
    wait :
         (Default value = 3)

    Returns
    -------

    """
    soup = None
    for _ in range(tries):
        try:
            request = Request(link)
            for k, v in headers.items():
                request.add_header(k, v)
            site = urlopen(request, timeout=timeout)
            soup = BeautifulSoup(site.read().decode('utf-8'), 'html.parser')
            # print(soup)
            # print(site.status)
            # print(site.info()) # Exibe o cabeçalho de resposta
            # print(chardet.detect())
            break
        except socket.timeout:
            time.sleep(wait)
        except HTTPError:
            pass
    return soup

def get_id_from_url(url):
    """

    Parameters
    ----------
    url :
        

    Returns
    -------

    """
    split_by = '-' if '-' in url else '.'
    return url.split('/')[-1].split(split_by)[0]

def save_soup(soup):
    with open('soup.html', 'w', encoding='utf-8') as file:
        file.write(str(soup))