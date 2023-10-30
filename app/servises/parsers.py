import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type
from urllib.parse import urlparse, urlunparse

from bs4 import BeautifulSoup, Tag

from bookmarks_app.models import Bookmark
from .scrapers import BaseHTMLPageScraper, RequestHTMLPageScraper


@dataclass
class ParamsMarkup:
    """Параметры разметки страницы"""

    title: str | None = None
    description: str | None = None


class BaseMarkupParser(ABC):
    """Базовый класс прсера разметки странцы с использованием BeautifulSoup"""

    def __init__(self, soup: BeautifulSoup):
        self.soup = soup

    @abstractmethod
    def get_title(self) -> str | None:
        raise NotImplementedError

    @abstractmethod
    def get_description(self) -> str | None:
        raise NotImplementedError


class OpenGraphMarkupParser(BaseMarkupParser):
    """Парсер Open Graph разметки страницы"""

    def get_title(self) -> str | None:
        meta = self.soup.find(name="meta", attrs={"property": "og:title"})
        if isinstance(meta, Tag):
            return meta.attrs["content"]
        return None

    def get_description(self) -> str | None:
        meta = self.soup.find(name="meta", attrs={"property": "og:description"})
        if isinstance(meta, Tag):
            return meta.attrs["content"]
        return None


class JSONLDMarkupParser(BaseMarkupParser):
    """Парсер JSON-LD разметки страницы"""

    def __init__(self, soup: BeautifulSoup):
        super().__init__(soup)
        self.__json_markup = None

    def _find_key_in_json(self, json_data, target_key) -> str | None:
        """Поиск значения по ключу в словаре хронящем структуру json"""
        if isinstance(json_data, dict):
            for key, value in json_data.items():
                if key == target_key:
                    return value
                elif isinstance(value, (dict, list)):
                    result = self._find_key_in_json(value, target_key)
                    if result is not None:
                        return result
        elif isinstance(json_data, list):
            for item in json_data:
                result = self._find_key_in_json(item, target_key)
                if result is not None:
                    return result
        return None

    @property
    def json_markup(self) -> dict:
        """Получение json с параметрами разметки"""
        if self.__json_markup is None:
            elm = self.soup.find(name="script", attrs={"type": "application/ld+json"})
            if isinstance(elm, Tag):
                self.__json_markup = json.loads(elm.text)
        return self.__json_markup or {}

    def get_title(self) -> str | None:
        return self._find_key_in_json(self.json_markup, target_key="title")

    def get_description(self) -> str | None:
        return self._find_key_in_json(self.json_markup, target_key="description")


class MetaMarkupParser(BaseMarkupParser):
    """Парсер мета разметки страницы"""

    def get_title(self) -> str | None:
        title = self.soup.find(name="title")
        if title:
            return title.text
        return None

    def get_description(self) -> str | None:
        for meta in self.soup.find_all(name="meta", attrs={"name": "description"}):
            return meta.attrs["content"]
        return None


class BookmarkParsingManager:
    markup_parsers: list[Type[BaseMarkupParser]] = [
        OpenGraphMarkupParser,
        JSONLDMarkupParser,
        MetaMarkupParser,
    ]

    def __init__(
        self,
        bookmark: Bookmark,
        scraper: Type[BaseHTMLPageScraper] = RequestHTMLPageScraper,
    ):
        self.bookmark = bookmark
        self.url = bookmark.bookmark_url
        self.scraper = scraper(url=self.url)
        self._determination_soup()
        self._parse_url()

    def _determination_soup(self, html_content: str | None = None):
        """Определение переменной хранящей класс BeautifulSoup для данной страницы"""
        if html_content is None:
            html_content = self.scraper.get_html()
        self.soup = BeautifulSoup(html_content, "lxml")

    def _parse_url(self, url: str | None = None):
        """Парсинг URL и сохранение переменных хранящих значение схемы и домена"""
        if url is None:
            url = self.url
        parse_url = urlparse(url)
        self.scheme_url = parse_url.scheme
        self.domain = parse_url.netloc

    def parse_and_save(self):
        """Парсинг и сохранение данных в БД"""
        params_marcup = self.get_params_marcup()
        self.bookmark.title = params_marcup.title
        self.bookmark.description = params_marcup.description
        self.bookmark.favicon_url = self.get_favicon_url()
        self.bookmark.save()
        return self.bookmark

    def get_params_marcup(self) -> ParamsMarkup:
        """Получение параметров разметки страницы"""
        params_marcup = ParamsMarkup()
        for markup_parser in self.markup_parsers:
            parser = markup_parser(soup=self.soup)
            if params_marcup.title is None:
                params_marcup.title = parser.get_title()
            if params_marcup.description is None:
                params_marcup.description = parser.get_description()
        return params_marcup

    def get_favicon_url(self) -> str | None:
        """Получение ссылки на фавикон"""
        favicon = self.soup.find(name="link", attrs={"rel": "shortcut icon"})
        if isinstance(favicon, Tag):
            href = favicon.attrs["href"]
        else:
            href = "/favicon.ico"
        return urlunparse((self.scheme_url, self.domain, href, "", "", ""))
