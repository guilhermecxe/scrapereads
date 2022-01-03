from scrapereads.goodreads_scrape.goodreads_scrape import get_book_infos, get_choice_awards_categories
import pytest

class TestGetBookInfos(object):
    def test_get_book_infos_nonexistent_id(self):
        actual = get_book_infos(id='531453556')
        assert actual is None

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

class TestGetChoiceAwardsCategories(object):
    def test_get_choice_awards_categories_with_int(self):
        expected_categories_amount = 22
        expected_categories_keys = ['Favorite Book of 2011', 'Nonfiction', "Middle Grade & Children's"]
        expected_categories_values = ['favorite-book-of', 'nonfiction-books', 'childrens-books']
        actual = get_choice_awards_categories(2011)
        assert len(actual) == expected_categories_amount
        for key in expected_categories_keys:
            assert key in actual.keys(), f"Was expected that {key} was one of the keys, but it wasn't"
        for value in expected_categories_values:
            assert value in actual.values(), f"Was expected that {value} was one of the values, but it wasn't"

    def test_get_choice_awards_categories_with_str(self):
        expected_categories_amount = 20
        expected_categories_keys = ['Fiction', 'Fantasy', 'Young Adult Fantasy']
        expected_categories_values = ['fiction-books', 'fantasy-books', 'young-adult-fantasy-books']
        actual = get_choice_awards_categories('2014')
        assert len(actual) == expected_categories_amount
        for key in expected_categories_keys:
            assert key in actual.keys(), f"Was expected that {key} was one of the keys, but it wasn't"
        for value in expected_categories_values:
            assert value in actual.values(), f"Was expected that {value} was one of the values, but it wasn't"

    def test_get_choice_awards_categories_with_invalid_year(self):
        actual = get_choice_awards_categories(1999)
        assert actual is None