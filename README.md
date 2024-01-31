# habrscapper

Этот репозиторий содержит проект по скрэйпингу и последующему анализу заголовков и 
текстов с habr, чтобы в дальнейшем применить методы машинного обучения и обработки 
естественных языков.

## scraputils

Пакет для всех инструментов по скрэйпингу с harb. Пример применения: 

```python
from scraputils import scrape_daily

scrape_daily()  # add today's news to the db

```

Если есть желание самостоятельно создать загрузчик данных 
```python
from scraputils import scrape_habr


def my_foo(row: list[str]):
    # load the data point to your destination
    # must be able to work in a pool
    pass


scrape_habr(my_foo, "https://habr.com/ru/articles/top/annual/page{}")

```
