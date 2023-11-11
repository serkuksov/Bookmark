import time
from abc import ABC, abstractmethod

import requests


class BaseHTMLPageScraper(ABC):
    """Базовый класс скраперов страниц"""

    def __init__(self, url: str):
        self.url = url

    @abstractmethod
    def get_html(self) -> str:
        raise NotImplementedError


class RequestHTMLPageScraper(BaseHTMLPageScraper):
    """Скрапер страницы с использованием библиотеки requests"""

    def get_html(self) -> str:
        response = requests.get(self.url)
        time.sleep(20)
        response.raise_for_status()
        return response.text
