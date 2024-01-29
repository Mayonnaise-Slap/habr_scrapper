import requests
from bs4 import BeautifulSoup
import re
import datetime
from db import habr_news, session


def get_soup(n_page: int) -> BeautifulSoup:
    link = fr"https://habr.com/ru/articles/top/weekly/page{n_page}/"
    r = requests.get(link)
    if r.status_code != 200:
        raise Exception("Something was wrong with the link")
    return BeautifulSoup(r.text, "html.parser")


def get_contents(soup: BeautifulSoup) -> list[list]:
    headings = []
    for article in soup.find_all("article"):
        info = get_heading(article)
        info.append(f"https://habr.com{article.find_all("a")[2]["href"]}")
        headings.append(info)
    return headings


def get_heading(article: BeautifulSoup) -> list[str]:
    score_index = 2

    heading = article.find_all("span")[2].text
    attrs = article.find_all("title")
    if len(attrs) == 6:
        score_index += 1
    rez = re.findall(r"[-+]?(?:\d*\.*\d+)", attrs[score_index].text)[1:]
    rez.insert(0, heading)
    return rez


def get_article_text(article_link: str) -> str:
    response = requests.get(article_link)
    if response.status_code != 200:
        raise Exception("foobar")
    soup = BeautifulSoup(response.text, "html.parser")

    return "\n".join(
        tag_contents.text.replace("&shy", '')
        .replace(";\xad","")
        .replace("\xad","")
        .replace(u"\xa0", " ")
        for tag_contents in soup.find(
            "div", {"class": "article-formatted-body"}
        ).contents)


def dump_heading(headings: list[list]) -> None:
    with session() as _session:
        for row in headings:
            entry = habr_news(
                title=row[0],
                upotes=row[1],
                downvotes=row[2],
                url=row[3],
                text=get_article_text(row[3]),
                date=datetime.date.today()
            )
            _session.add(entry)
        _session.commit()


def main(pages: range) -> None:
    for i in pages:
        dump_heading(get_contents(get_soup(i + 1)))


if __name__ == "__main__":
    main(range(1, 13))
