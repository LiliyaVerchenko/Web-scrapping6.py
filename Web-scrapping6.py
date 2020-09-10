import requests
from bs4 import BeautifulSoup
from pprint import pprint

# получаем полные тексты статей, включая заголовки и хабы
def get_articles_with_keywords():
    response = requests.get('https://habr.com/ru/all/')
    bs = BeautifulSoup(response.text, 'html.parser')
    article = bs.find_all('article', class_='post')
    # извлекаем статьи
    for art in article:
        #  получаем название статьи
        article_title = art.find('a', class_='post__title_link')

        # получаем список хабов
        article_hub = art.find_all('a', class_='hub-link')
        hubs_link = list(map(lambda hub: hub.text.lower(), article_hub))

        # получаем ссылку на статью
        article_link = article_title.attrs.get('href')

        # переходим на страницу статьи
        response_read_more = requests.get(article_link)
        bs1 = BeautifulSoup(response_read_more.text, 'html.parser')

        # получаем полный текст статьи
        article_text_full = bs1.find('div', class_='post__text')

        # получаем дату статьи
        date_info = bs1.find('span', class_='post__time')
        date_article = date_info.attrs.get('data-time_published')[0:10]

        # находим пересечения статей с ключевыми словами
        for word in KEYWORDS:
            if word in article_title.text.lower() or word in hubs_link or word in article_text_full.text.lower():
                print(f'<{date_article}> - {article_title.text} - <{article_link}>')
    return 'Получен перечень статей, в которых встречаются слова из KEYWORDS'

if __name__ == '__main__':
    KEYWORDS = ['дизайн', 'фото', 'web', 'python']
    print(get_articles_with_keywords())




