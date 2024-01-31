import requests
from bs4 import BeautifulSoup
import re
import datetime
from db import habr_news, session
import multiprocessing as mp


def get_soup(page_link: str) -> BeautifulSoup:
    """
    Standard requests+bs4 helper function
    Args:
        page_link (): string url to a specific page
    Returns:
        BeautifulSoup of the page
    """
    r = requests.get(page_link)
    if r.status_code != 200:
        raise Exception(f"Something was wrong with the link {page_link}")
    return BeautifulSoup(r.text, "html.parser")


def get_contents(soup: BeautifulSoup) -> list[list]:
    """
    Scrapes the primary page
    Args:
        soup (): soup that is the primary
        page on url like https://habr.com/top/daily/page{}
    Returns:
    A list of article titles, their scores and links
    """
    headings = []
    for article in soup.find_all("article"):
        info = get_heading(article)
        info.append(f"https://habr.com{article.find_all("a")[2]["href"]}")
        headings.append(info)
    return headings


def get_heading(article: BeautifulSoup) -> list[str]:
    """
    Scrapes title and scores
    Args:
        article (): soup that is in <article> tag
    Returns:
    A list of article titles and their scores
    """
    score_index = 2

    heading = article.find_all("span")[2].text
    attrs = article.find_all("title")
    if len(attrs) == 6:
        score_index += 1
    rez = re.findall(r"[-+]?(?:\d*\.*\d+)", attrs[score_index].text)[1:]
    rez.insert(0, heading)
    return rez


def get_article_text(article_link: str) -> str:
    """
    This function takes a link to an article on habr and
    returns the article in plain text. It does not save
    pictures or links, only plain text is returned.
    Args:
        article_link (): A link to a habr article

    Returns:
    text (str): The article's plain text
    """
    response = requests.get(article_link)
    if response.status_code != 200:
        raise Exception("foobar")
    soup = BeautifulSoup(response.text, "html.parser")

    return "\n".join(
        tag_contents.text.replace("&shy", "")
        .replace(";\xad", "")
        .replace("\xad", "")
        .replace("\xa0", " ")
        for tag_contents in soup.find(
            "div", {"class": "article-formatted-body"}
        ).contents
    )


def dump_page(page_link: str, foo) -> None:
    """
    Methods that uploads scraped data to the database
    Args:
        foo (): function to dump in parallel
        page_link: link to the page to be processed
    """
    headings = get_contents(get_soup(page_link))

    print(f"Scraping {len(headings)} articles")
    _pool = mp.Pool()
    _pool.map(foo, headings)
    _pool.close()


def db_dump(row: list) -> None:
    """
    function to dump scraped data to the sqlite database
    """
    _session = session()
    article_text = get_article_text(row[3])
    entry = habr_news(
        title=row[0],
        upvotes=row[1],
        downvotes=row[2],
        url=row[3],
        text=article_text,
        date=datetime.date.today(),
    )
    _session.add(entry)
    _session.commit()
    _session.close()


def find_number_of_pages(base_link: str) -> int:
    """
    Scrapes habr's first page to find how many
    pages there are to scrape
    Args:
        base_link (): a template string that .format(int) can be called onto

    Returns:
        number of pages that can be parsed
    """
    soup = get_soup(base_link.format(1))
    n_pages = int(soup.find_all("a",
                                {"class": "tm-pagination__page"})[-1].text)
    print(f"Found {n_pages} news pages")
    return n_pages


def foo_dump(row: list) -> None:
    """
    placeholder dump method for testing
    """
    get_article_text(row[3])
    pass


def scrape_habr(foo, page_link: str) -> None:
    """
    main method that dumps all news pages and texts to the db

    Args:
        foo ():
        page_link: forgettable string of https://habr.com/ru/articles/top{something}/page{}/ to scrape
    """
    for n_page in range(find_number_of_pages(page_link)):
        dump_page(page_link.format(n_page + 1), foo)
        print(f"Dumped {n_page+1} page")


if __name__ == "__main__":
    link = r"https://habr.com/ru/articles/top/weekly/page{}/"
    scrape_habr(db_dump, link)
