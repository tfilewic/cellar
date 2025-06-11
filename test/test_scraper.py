"""
Rating scraper tests

"""

import pytest
from app import app
from unittest.mock import patch, Mock
from scraper.scraper import scrape_rating



def test_scraper_live_site(client, data2):
    expected = 90
    payload = {
        "name": "Red Icon",
        "vintage": "2018",
        "producer_id": 1
    }
    client.post("/wines", json=payload)
    response = client.get("/wines")

    rating = response.get_json()[0]["rating"]
    assert rating == expected


def test_scraper_saved_html():
    expected = 90

    with open("test/CellarTracker.html", "r") as f:
        html = f.read()

    response = Mock()
    response.status_code = 200
    response.text = html

    with patch('requests.get', return_value=response):
        rating = scrape_rating("anyname", "anyvintage", "anyproducer")
        assert rating == expected
