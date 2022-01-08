# Scrapereads

**Trying to make this package the more professional that I can, but be known that it is being made by a beginner :)** 


Scrapereads is a package used to get informations about books via web scraping.

## Features

* Written in Python 3 (compatible with Python 3.6, 3.7, 3.8 and 3.9)

## Examples

```py
>>> from scrapereads import get_choice_awards_categories
>>> get_choice_awards_categories(2015)
'''
get_choice_awards_categories(year)
    Get all Goodreads Choice Awards categories from a given year.

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
'''
```

```py
>>> from scrapereads import get_book_infos
>>> clap_when_you_land = get_book_infos(id='52516332')
>>> clap_when_you_land.keys()
dict_keys(['id', 'editions id', 'title', 'author', 'published year', 'rating', 'ratings', 'genres', 'synopsis'])
>>> clap_when_you_land['title']
'Clap When You Land'
>>> clap_when_you_land['author']
'Elizabeth Acevedo (Goodreads Author)'
>>> clap_when_you_land['genres']
['Young Adult', 'Contemporary', 'Poetry', 'Fiction', 'Audiobook', 'LGBT', 'Realistic Fiction', 'Family', 'LGBT', 'Queer', 'Young Adult', 'Young Adult Contemporary']
```

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
