import requests as req
from bs4 import BeautifulSoup
import string


def get_title(soup):
    title = soup.find('h1', {'class': 'c-article-magazine-title'}).text
    title_punc = title.translate(title.maketrans('', '', string.punctuation))

    return title_punc.translate(title_punc.maketrans(' ', '_'))  # Replace spaces with _


def get_body(soup):
    body = soup.find('div', {'class': 'c-article-body u-clearfix'}).text.strip()

    return body


def save_file(title, body):
    file = open(f'{title}.txt', 'w', encoding='UTF-8')
    file.write(body)
    file.close()


def main():
    url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3"
    r = req.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})

    if r.status_code != 200:
        print(f"The URL returned {r.status_code}!")
    else:
        soup = BeautifulSoup(r.content, 'html.parser')
        articles = soup.find_all('article')

        for article in articles:
            articles_type = article.find(
                'span', {'data-test': 'article.type'}
            ).find('span')

            if articles_type.text == 'News':
                get_link = article.find(
                    'a', {'data-track-action': 'view article'}
                )
                r = req.get(f"https://www.nature.com{get_link.get('href')}")
                soup = BeautifulSoup(r.content, 'html.parser')

                title, body = get_title(soup), get_body(soup)
                save_file(title, body)


if __name__ == "__main__":
    main()
