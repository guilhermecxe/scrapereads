from scrapereads.goodreads_scrape.utils import get_soup, get_id_from_url, save_soup
import re

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

def get_book_infos(id=None, url=None):
    """Get informations from a book

    Parameters
    ----------
    id : {str, None}
        (Default value = None)
        The book identification code used by Goodreads. If `url` is `None`, then `id` must
        be specified.
    url : {str, None}
        (Default value = None)
        Link to a book page on Goodreads. If `id` is `None`, then `url` must
        be specified.

    Returns
    -------
    dict
        All available book informations.
    None
        If `HTTPError` when trying to get the book page, then the result is `None`.
    """
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
    """Get all Goodreads Choice Awards categories from a given year.

    Parameters
    ----------
    year : {int, str}
        Some year that happened the Goodreads Choice Awards.

    Returns
    -------
    dict
        All categories from the given year. With categories names as keys and categories codes as values.
    None
        If `HTTPError` when trying to get the Choice Awards page, then the result is `None`.
    """
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

def get_choice_awards_nominees(year, category):
    """Get the Goodreads Choice Awards nominees for the given year and category.

    Parameters
    ----------
    category : str
        Code of a category that was on Goodreads Choice Awards for the given year.
    year : {int, str}
        Some year that happened the Goodreads Choice Awards.

    Returns
    -------
    list
        List with all books found represented as dictionaries.
    """
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