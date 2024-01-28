import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


def get_soup(n_page: int) -> BeautifulSoup:
    link = fr"https://habr.com/ru/articles/top/weekly/page{n_page}/"
    r = requests.get(link)
    if r.status_code != 200:
        raise Exception("banned")
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


def dump_heading(headings: list[list]) -> None:
    df = pd.DataFrame(headings, columns=["Heading", "up", "down", "link"])
    df["text"] = df["link"].apply(get_article_text)
    df["date"] = pd.Timestamp.today().date()
    df.to_csv("headings.csv", mode="a", index=False, header=False)


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


def main(pages: range) -> None:
    for i in pages:
        dump_heading(get_contents(get_soup(i + 1)))
        # time.sleep(1)


# while True:
main(range(2, 17))

# time.sleep(86400)
