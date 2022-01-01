from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import socket
import time

def get_id_from_url(url):
    split_by = '.' if '.' in url else '-'
    return url.split(split_by)[0].split('/')[-1]

def get_soup(link, tries=3, timeout=10, wait=3):
    for _ in range(tries):
        try:
            site = urlopen(link, timeout=timeout)
            soup = BeautifulSoup(site.read(), 'html.parser')
            break
        except socket.timeout:
            time.sleep(wait)
    return soup

def get_book_infos(id=None, url=None):
        if not id:
            id = get_id_from_url(url)

        soup = get_soup(f'https://www.goodreads.com/book/show/{id}')

        title = soup.find(id='bookTitle').get_text().strip()
        author = soup.find(class_='authorName__container').parent.get_text().strip()
        rating = soup.find('span', {'itemprop': 'ratingValue'}).get_text().strip()
        ratings = soup.find(attrs={'itemprop': 'ratingCount'}).get('content')

        try:
            synopsis = soup.find(id='description').find_all('span')[-1].get_text()
        except AttributeError:
            return None

        editions_id = get_id_from_url(soup.find('a', text=re.compile('All Editions')).get('href'))
        
        details = soup.find(id='details').find_all('div')[1].get_text()
        result = re.search('[1-3][0-9]{3}', details)
        year = None if result is None else result.group()

        genres_elements = soup.find_all('a', {'href': re.compile('/genres/')}, class_='bookPageGenreLink')
        genres = list(map(lambda element: element.get_text(), genres_elements))

        book_dict = {}
        book_dict['title'] = title
        book_dict['id'] = id
        book_dict['author'] = author
        book_dict['rating'] = rating
        book_dict['ratings'] = ratings
        book_dict['synopsis'] = synopsis
        book_dict['published'] = year
        book_dict['genres'] = genres
        book_dict['editions id'] = editions_id

        return book_dict

if __name__ == '__main__':
    print(get_book_infos(id='53145356'))