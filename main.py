from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import re

# поисковый запрос на сайте habr.com. параметры: number - номер страницы, search - текст поискового запроса
list_url = "https://habr.com/ru/search/page{number}/?q={search}&target_type=posts&order=relevance"

# текст поискового запроса
search_text = "javascript"

# кол-во страниц
max_page_number = 2

# номер стартовой страницы
page_number = 1


class Article:
    def __init__(self, code):
        # заголовок статьи
        self.title = code.h2.span.getText()
        # теги статьи
        self.tags = code.find('div', {'class': 'tm-article-snippet__hubs'}).getText()
        # краткое описание статьи
        self.description = code.find('div', {'class': 'article-formatted-body'}).getText()
        # автор статьи(удаляем лишние пробелы/отступы)
        raw_author = code.find('a', {'class': 'tm-user-info__username'}).getText()
        self.author = re.sub(r"[\n\t\s]* +", " ", raw_author)
        # ссылка на статью из заголовка
        self.link = 'https://habr.com' + code.h2.a['href']
        # дата публикации статьи
        self.date = code.time.getText()

    def get_data(self):
        return [
            self.title,
            self.tags,
            self.description,
            self.author,
            self.date,
            self.link
        ]


# список полученных данных статей
article_list = []

while page_number <= max_page_number:
    url = list_url.format(number=page_number, search=search_text)
    html = urlopen(url)
    bs = BeautifulSoup(html.read(), 'html.parser')
    for article in bs.findAll('article'):
        article_list.append(Article(article))
    page_number += 1

# сохранение результата в csv файл
with open("results.csv", "w", newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=';')
    for article in article_list:
        writer.writerow(article.get_data())
