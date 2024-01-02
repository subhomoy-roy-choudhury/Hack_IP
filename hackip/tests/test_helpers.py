import pytest
from hackip.helpers import get_shortened_url, get_size, encoding_result, slug_to_title
from unittest.mock import patch

def test_get_size():
    assert get_size(1023) == "1023.00B"
    assert get_size(1024) == "1.00KB"
    assert get_size(1048576) == "1.00MB"
    # Add more assertions as needed

def test_encoding_result():
    test_dict = {"key": "value"}
    result = encoding_result(test_dict)
    # Check if result is a base64 encoded string
    # Add more test cases

@patch('hackip.helpers.requests.get')
def test_get_shortened_url(mock_get):
    pass
    # Setup mock response
    # Test success scenario
    # Test failure scenario
    # Add more test cases

def test_slug_to_title():
    assert slug_to_title("hello-world") == "Hello World"
    assert slug_to_title("test") == "Test"
    # Add more test cases