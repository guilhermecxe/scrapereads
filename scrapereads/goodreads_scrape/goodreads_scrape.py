from scrapereads.goodreads_scrape.utils import get_soup, get_id_from_url
import re

def get_synopsis_from_soup(soup):
    try:
        return soup.find(id='description').find_all('span')[-1].get_text()
    except AttributeError:
        return None

def get_published_year_from_soup(soup):
    details = soup.find(id='details').find_all('div')[1].get_text()
    result = re.search('[1-3][0-9]{3}', details)
    return None if result is None else int(result.group())

def get_genres_from_soup(soup):
    genres_elements = soup.find_all('a', {'href': re.compile('/genres/')}, class_='bookPageGenreLink')
    return list(map(lambda element: element.get_text(), genres_elements))

def get_book_infos(id=None, url=None):
        if not id:
            id = get_id_from_url(url)
        
        soup = get_soup(f'https://www.goodreads.com/book/show/{id}')
        if soup is None:
            return None

        book_dict = {
            'id': id,
            'editions id': get_id_from_url(soup.find('a', text=re.compile('All Editions')).get('href')),
            'title': soup.find(id='bookTitle').get_text().strip(),
            'author': soup.find(class_='authorName__container').parent.get_text().strip(),
            'published year': get_published_year_from_soup(soup),
            'rating': soup.find('span', {'itemprop': 'ratingValue'}).get_text().strip(),
            'ratings': soup.find(attrs={'itemprop': 'ratingCount'}).get('content'),
            'genres': get_genres_from_soup(soup),
            'synopsis': get_synopsis_from_soup(soup)
        }

        return book_dict

def get_choice_awards_categories(year):
    soup = get_soup(f'https://www.goodreads.com/choiceawards/best-books-{year}')
    if soup is None:
        return None
        
    genres_divs = soup.find_all('div', class_='category clearFix')
    get_genre_from_link = lambda link: link.split('/')[-1][5:-5] if 'best' in link else link.split('/')[-1][:-5]

    genres = {}
    for genre_div in genres_divs:
        key = genre_div.find('h4').get_text().strip()
        value = get_genre_from_link(genre_div.a.get('href'))
        genres[key] = value

    return genres

def get_choice_awards_nominees(category, year):
    if not 'favorite' in category:
        category = 'best-' + category
    link = f'https://www.goodreads.com/choiceawards/{category}-{year}'
    soup = get_soup(link)
    if soup is None:
        raise ValueError(
            f"Category or year invalid. See get_choice_awards_categories({year}).values() "
            "to get available categories for the year")

    books = soup.find_all('a', id=re.compile('bookCover'))
    books_dicts = []
    for book in books:
        book_dict = {
            'id': get_id_from_url(book.get('href')),
            'title and author': book.img.get('alt'),
            'img': book.img.get('src')
        }
        books_dicts.append(book_dict)

    return books_dicts