from typing import Any
from abc import ABCMeta, abstractmethod, ABC
import requests
from bs4 import BeautifulSoup
from requests import get
from .WP_Poster import CreatePost
import threading, queue
import json


def __getContent(url):
    response = get(url)
    if response.status_code == 200:
        content_soup = BeautifulSoup(response.text, "html.parser")
        title = content_soup.select_one("#headlineitem")
        content = content_soup.select_one(".article-full-content")
        date_posted = content_soup.select_one("a+ span")
        images = content_soup.select(".article-img img , .wp-image-10082631")
        print(title.text.strip())
        # print(content.text)
        print(date_posted.text.strip())
        print(len(images))
        print(date_posted.text)
        CreatePost(title.text, str(content), "2020-01-05T10:00:00")
        for i in images:
            if i.get("data-src" or None):
                print(i["data-src"])
            else:
                print(i["src"])


def getNews():
    css = ".main-title a"
    response = get("https://www.firstpost.com/category/sports")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        titles = soup.select(css)
        print(f"total collected titles {len(titles)}")
        titles_queue = queue.Queue(maxsize=30)
        for i in titles:
            # print(i.text)
            # print(i['href'])
            titles_queue.put(i["href"], timeout=3)
            thread = threading.Thread(target=__getContent, args=(titles_queue.get(),))
            thread.start()


class ABC_NEWS(metaclass=ABCMeta):
    @abstractmethod
    def getNewsAsJson(self):
        """scrap news and return it as json"""


class SkySportNewsExtractor(ABC_NEWS, ABC):
    def __init__(self, source_page, css_selector, callback) -> None:
        print("Initializing SkySportNewsExtractor")
        self.source_page = source_page
        self.soup = BeautifulSoup(source_page, "html.parser")
        self.css_selector = css_selector
        self.callback = callback

    def contentExtractor(self, url):
        #TODO add all p togather and add a breakline
        css_selector = "div > div p"
        html_content = self.callback(url)
        content_soup = BeautifulSoup(html_content, "html.parser")
        return content_soup.select_one(css_selector)

    def getNewsAsJson(self) -> list:

        titles = self.soup.select(self.css_selector)
        news_container = []
        if all([len(titles) > 0, titles]):
            for news in titles:
                try:
                    print(news.text.strip(), "\n", news["href"])
                    content = self.contentExtractor(news["href"])
                    news_container.append(
                        dict(
                            title=news.text.strip(),
                            link=news["href"],
                            content_string=content.text,
                            content_obj=content,
                        )
                    )
                except Exception as e:
                    print(e)
                    pass
            pass
        else:
            print("No data was found")
        return news_container


class FirstPostNewsExtractors(ABC_NEWS, ABC):
    def __init__(self, source_page, css_selector) -> None:
        print("Initializing FirstPostNewsExtractors")

        self.soup = BeautifulSoup(source_page, "html.parser")
        self.css_selector = css_selector

    def __repr__(self):
        return """A first post sport news extract"""

    def getNewsAsJson(self) -> list:
        titles = self.soup.select(selector=self.css_selector)
        news_container = []
        if all([len(titles) > 0, titles]):
            for news in titles:
                news_container.append(dict(title=news.text, link=news["href"]))
            pass
        return news_container


class NewsResources:
    def __init__(self):
        pass

    @staticmethod
    def GetWebPageSource(url: str) -> str:
        response = get(url)
        if response.status_code == 200:
            print("Source Page extracted successfully")
            return response.text
        else:
            return False

    def SkySport(self):
        """Scrap news from https://www.skysports.com/football/news"""

        html_response = self.GetWebPageSource(
            url="https://www.skysports.com/football/news"
        )
        trend_selector = ".news-list__headline-link"
        if html_response:
            sky_news = SkySportNewsExtractor(
                source_page=html_response,
                css_selector=trend_selector,
                callback=self.GetWebPageSource,
            )
            return sky_news.getNewsAsJson()
        else:
            print("Could not fetch html from https://skynews.com")

    def FirstPost(self):
        """Scrap news from https://www.firstpost.com"""
        headlines_selector = ".main-title a"
        html_response = self.GetWebPageSource(
            url="https://www.firstpost.com/category/sports"
        )
        if html_response:
            firstPostNews = FirstPostNewsExtractors(
                source_page=html_response, css_selector=headlines_selector
            )
            return firstPostNews.getNewsAsJson()
        else:
            print("Could not fetch html from https://www.firstpost.com")


if __name__ == "__main__":
    news = NewsResources()
    print(news.SkySport())
