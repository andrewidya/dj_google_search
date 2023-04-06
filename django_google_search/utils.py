from typing import Optional
from time import sleep
import requests
from bs4 import BeautifulSoup
from requests import Response

from django_google_search.user_agents import get_useragent


def make_requests(term: str, offset: int, start: int,
                  lang: str = "en", date_filter: Optional[str] = None,
                  proxies: Optional[dict] = None) -> Response:
    params = dict(
        q=term,
        num=offset + 2,
        hl=lang,
        start=start
    )

    if date_filter:
        params.update({"as_qdr": date_filter})

    resp = requests.get(
        url="https://www.google.com/search",
        headers={
            "User-Agent": get_useragent()
        },
        params=params,
        proxies=proxies,
    )
    resp.raise_for_status()

    return resp


class SearchResult:
    def __init__(self, url: str, title: str, description: Optional[str] = None):
        self.url = url
        self.title = title
        self.description = description

    def __str__(self):
        return f"SearchResult(url={self.url}, title={self.title}, description={self.description})"


def search(term: str, num_results: int = 10, lang: str = "en",
           date_filter: Optional[str] = None, proxy: Optional[dict] = None,
           sleep_interval: int = 2):
    escape_term = term.replace(" ", "+")

    proxies = None
    if proxy:
        if proxy.startwith("https"):
            proxies = {"https": proxy}
        else:
            proxies = {"http": proxy}

    start = 0
    while start < num_results:
        offset = num_results - start
        response = make_requests(escape_term, offset, start, lang, proxies)

        soup = BeautifulSoup(response.text, "html.parser")
        elements = soup.find_all("div", attrs={"class": "ezO2md"})

        for elem in elements:
            link = elem.find("a", href=True)

            if not link:
                continue

            title = link.find("span", attrs={"class": "CVA68e qXLe6d fuLhoc ZWRArf"})
            description = ""

            dsc_box = elem.find_all("div", {"class": "Dks9wf"})
            if dsc_box:
                descs = dsc_box[0].find_all("span", attrs={"class": "fYyStc"})
                if descs:
                    description = descs[-1].text if len(descs) > 1 else descs[0].text
                else:
                    description = ""

            if link and title:
                start += 10
                yield SearchResult(link.attrs.get("href"), title.text, description)

        sleep(sleep_interval)
