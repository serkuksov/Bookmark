import unittest
from unittest.mock import patch
from services.scrapers import RequestHTMLPageScraper


class TestRequestHTMLPageScraper(unittest.TestCase):
    def test_init(self):
        url = "https://test.com"
        scraper = RequestHTMLPageScraper(url)
        self.assertEqual(scraper.url, url)

    @patch("requests.get")
    def test_get_html(self, mock_get):
        url = "https://test.com"
        expected_html = "<html><body>TEST</body></html>"

        mock_response = mock_get.return_value
        mock_response.text = expected_html

        scraper = RequestHTMLPageScraper(url)
        html = scraper.get_html()
        self.assertEqual(html, expected_html)
