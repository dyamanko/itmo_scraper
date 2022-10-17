def parse(url):
    print(url)


# поисковый запрос на сайте habr.com. параметры: number - номер страницы, search - текст поискового запроса
list_url = "https://habr.com/ru/search/page{number}/?q={search}&target_type=posts&order=relevance"

# текст поискового запроса
search_text = "javascript"

# кол-во страниц
max_page_number = 20

# номер стартовой страницы
page_number = 1


while page_number <= max_page_number:
    parse(list_url.format(number=page_number, search=search_text))
    page_number += 1
