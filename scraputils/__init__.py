from scrapper import scrape_habr, db_dump, foo_dump, get_article_text
from db import session, habr_news


def test_scrape_custom_link(link: str) -> None:
    """
    A function that lets you test whether a custom link
    will work properly with the crapper and not throw.
    Args:
        link: formattable string
    """
    scrape_habr(foo_dump, link)


def db_scrape_custom_link(link: str) -> None:
    """
    The function will dump the scraped page to the db.
    Allows for a custom link to be used
    Args:
        link (): a formattable string
    """
    scrape_habr(db_dump, link)


def scrape_daily() -> None:
    """
    Will dump the top daily articles to the sqlite db
    """
    link = "https://habr.com/ru/articles/top/daily/page{}"
    scrape_habr(db_dump, link)


def scrape_weekly() -> None:
    """
    Will dump the top weekly articles to the sqlite db
    """
    link = "https:habr.com/ru/articles/top/weekly/page{}"
    scrape_habr(db_dump, link)