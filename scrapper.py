import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


def get_soup(n_page: int) -> BeautifulSoup:
    link = fr"https://habr.com/ru/articles/top/daily/page{n_page}/"
    r = requests.get(link)
    if r.status_code != 200:
        raise Exception("banned")
    return BeautifulSoup(r.text, "html.parser")


def get_headings(soup: BeautifulSoup) -> list[list]:
    headings = []
    for article in soup.find_all("article"):
        score_index = 2

        heading = article.find_all("span")[2].text
        attrs = article.find_all("title")
        if len(attrs) == 6:
            score_index += 1
        rez = re.findall(r"[-+]?(?:\d*\.*\d+)", attrs[score_index].text)[1:]
        rez.insert(0, heading)
        headings.append(rez)
    return headings


def dump_heading(headings: list[list]) -> None:
    df = pd.DataFrame(headings, columns=["Heading", "up", "down"])
    df["date"] = pd.Timestamp.today().date()
    df.to_csv("headings.csv", mode="a", index=False, header=False)


if __name__ == "__main__":
    for i in range(4):
        dump_heading(get_headings(get_soup(i)))