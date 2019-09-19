import pytest
import os, sys
# Hack to allow importing from a sibling folder 
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from src.twitter_scraper import twitter_scraper



@pytest.fixture
def credentials_dict():
    return twitter_scraper.get_credentials_as_dict()


@pytest.fixture
def ids():
    return twitter_scraper.get_ids_and_labels_as_lists()[0]


@pytest.fixture
def sentiment_labels():
    return twitter_scraper.get_ids_and_labels_as_lists()[1]


def test_read_credentials_returns_dictionary_of_4_keys():
    credentials = twitter_scraper.get_credentials_as_dict()
    assert len(credentials.keys()) == 4


def test_credentials_is_a_dict(credentials_dict):
    assert isinstance(credentials_dict, dict)


credentials_names = [
    'CONSUMER_KEY', 'CONSUMER_SECRET', 'ACCESS_TOKEN', 'ACCESS_TOKEN_SECRET'
]


@pytest.mark.parametrize("credential_name", credentials_names)
def test_read_credentials_includes_credential_name(credential_name, credentials_dict):
    assert credential_name in credentials_dict


def test_read_values_are_strings_without_spaces_or_quotes(credentials_dict):
    list_of_data = list(credentials_dict.keys()) + \
        list(credentials_dict.values())
    for item in list_of_data:
        for unwanted_char in [' ', '"', "'", '\n', '\t']:
            if unwanted_char in item:
                assert False


lists = [
    twitter_scraper.get_ids_and_labels_as_lists()[0],
    twitter_scraper.get_ids_and_labels_as_lists()[1]
]
@pytest.mark.parametrize("list_variable", lists)
def test_returns_lists(list_variable):
    assert isinstance(list_variable, list)


def test_ids_and_sentiment_labels_are_the_same_length(ids, sentiment_labels):
    assert len(ids) == len(sentiment_labels)


def get_batch_to_process_returns_2_lists():
    a, b = twitter_scraper.get_batch_to_process()
    assert isinstance(a, list)
    assert isinstance(b, list)


def test_can_import_from_docs_folder():
    docs_path = twitter_scraper.get_docs_abs_path()
    assert docs_path == "c:\\Dev\\bootcamp\\twitter_api_exercise\\docs\\"

