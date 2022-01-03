from scrapereads.goodreads_scrape.goodreads_scrape import get_book_infos
import pytest

class TestGetBookInfos(object):
    def test_get_book_infos_nonexistent_id(self):
        expected = None
        actual = get_book_infos(id='531453556')
        assert actual == expected

    def test_get_book_infos_with_id(self):
        expected = {
            'id': '53145356',
            'editions id': '73359070',
            'title': 'Porém Bruxa',
            'author': 'Carol Chiovatto (Goodreads Author)',
            'published year': 2019
        }
        actual = get_book_infos(id='53145356')
        for key in ['id', 'editions id', 'title', 'author', 'published year']:
            assert actual[key] == expected[key], f'For the key "{key}" was expected {expected[key]}, but returned {actual[key]}'

    def test_get_book_infos_with_url(self):
        expected = {
            'id': '17601',
            'editions id': '881777',
            'title': 'The Will to Change: Men, Masculinity, and Love',
            'author': 'bell hooks',
            'published year': 2004
        }
        actual = get_book_infos(url='https://www.goodreads.com/book/show/17601.The_Will_to_Change')
        for key in ['id', 'editions id', 'title', 'author', 'published year']:
            assert actual[key] == expected[key], f'For the key "{key}" was expected {expected[key]}, but returned {actual[key]}'