import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time


def get_soup(n_page: int) -> BeautifulSoup:
    link = fr"https://habr.com/ru/articles/top/daily/page{n_page}/"
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
    df["date"] = pd.Timestamp.today().date()
    df.to_csv("headings.csv", mode="a", index=False, header=False)


def main():
    for i in range(4):
        dump_heading(get_contents(get_soup(i+1)))
        time.sleep(1)


if __name__ == '__main__':
    main()

# while True:
#     main()
#     time.sleep(86400)
