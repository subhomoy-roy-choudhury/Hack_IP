import pytest
import base64
from hackip.helpers import get_shortened_url, get_size, encoding_result, slug_to_title
from unittest.mock import patch


def test_zero_bytes():
    assert get_size(0) == "0.00B"


def test_bytes_less_than_kilobyte():
    assert get_size(512) == "512.00B"


def test_exactly_one_kilobyte():
    assert get_size(1024) == "1.00KB"


def test_bytes_just_less_than_megabyte():
    assert get_size(1048575) == "1024.00KB"


def test_exactly_one_megabyte():
    assert get_size(1048576) == "1.00MB"


def test_large_number_of_bytes():
    ten_gigabytes = 10 * 1024 * 1024 * 1024
    assert get_size(ten_gigabytes) == "10.00GB"


def test_extremely_large_byte_sizes():
    one_terabyte = 1024 * 1024 * 1024 * 1024
    assert get_size(one_terabyte) == "1.00TB"
    one_petabyte = 1024 * one_terabyte
    assert get_size(one_petabyte) == "1.00PB"


def test_with_simple_dictionary():
    dictionary = {"key": "value"}
    expected_output = base64.b64encode(str(dictionary).encode("UTF-8"))
    assert encoding_result(dictionary) == expected_output


def test_with_empty_dictionary():
    dictionary = {}
    expected_output = base64.b64encode(str(dictionary).encode("UTF-8"))
    assert encoding_result(dictionary) == expected_output


def test_with_nested_dictionary():
    dictionary = {"key": {"subkey": "value"}}
    expected_output = base64.b64encode(str(dictionary).encode("UTF-8"))
    assert encoding_result(dictionary) == expected_output


def test_with_various_data_types():
    dictionary = {"int": 1, "str": "test", "list": [1, 2, 3]}
    expected_output = base64.b64encode(str(dictionary).encode("UTF-8"))
    assert encoding_result(dictionary) == expected_output


def test_for_consistency():
    dictionary = {"key": "value"}
    output1 = encoding_result(dictionary)
    output2 = encoding_result(dictionary)
    assert output1 == output2


@patch("hackip.helpers.requests.get")
def test_successful_url_shortening(mock_get):
    mock_get.return_value.json.return_value = {
        "url": {"status": 7, "shortLink": "http://cutt.ly/shortenedUrl"}
    }
    shortened_url = get_shortened_url("http://example.com")
    assert shortened_url == "http://cutt.ly/shortenedUrl"


@patch("hackip.helpers.requests.get")
def test_failure_in_url_shortening(mock_get):
    mock_get.return_value.json.return_value = {"url": {"status": 1, "shortLink": None}}
    shortened_url = get_shortened_url("http://example.com")
    assert (
        shortened_url is None
    )  # or assert for an error message based on your implementation


@patch("hackip.helpers.requests.get")
def test_handling_invalid_url(mock_get):
    mock_get.return_value.json.return_value = {"url": {"status": 1, "shortLink": None}}
    shortened_url = get_shortened_url("invalid_url")
    assert (
        shortened_url is None
    )  # or assert for an error message based on your implementation


def test_with_standard_slug():
    assert slug_to_title("this-is-a-test-slug") == "This Is A Test Slug"


def test_with_empty_slug():
    assert slug_to_title("") == ""


def test_with_uppercase_letters():
    assert slug_to_title("This-Is-A-Test") == "This Is A Test"


def test_with_single_word_slug():
    assert slug_to_title("slug") == "Slug"


def test_with_numbers_and_special_characters():
    assert slug_to_title("test-slug-123-!@#") == "Test Slug 123 !@#"


def test_with_leading_and_trailing_hyphens():
    assert slug_to_title("-leading-trailing-") == " Leading Trailing "
