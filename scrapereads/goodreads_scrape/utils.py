from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import socket
import time
from scrapereads.configs import headers
import re

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

def get_synopsis_from_soup(soup):
    """Get the synopsis from a book page.

    Parameters
    ----------
    soup : BeautifulSoup
        BeautifulSoup object created from a book page.

    Returns
    -------
    str
        Book synopsis.
    None
        Synopsis not found.
    """
    try:
        return soup.find(id='description').find_all('span')[-1].get_text()
    except AttributeError:
        return None

def get_published_year_from_soup(soup):
    """Get the publication year of a book.

    Parameters
    ----------
    soup : BeautifulSoup
        BeautifulSoup object created from a book page.

    Returns
    -------
    int
        Book publication year.
    None
        Publication year not found.
    """
    details = soup.find(id='details').find_all('div')[1].get_text()
    result = re.search('[1-3][0-9]{3}', details)
    return None if result is None else int(result.group())

def get_genres_from_soup(soup):
    """Get the genres of a book.

    Parameters
    ----------
    soup : BeautifulSoup
        BeautifulSoup object created from a book page.

    Returns
    -------
    list
        Book genres.
    """
    genres_elements = soup.find_all('a', {'href': re.compile('/genres/')}, class_='bookPageGenreLink')
    return list(map(lambda element: element.get_text(), genres_elements))