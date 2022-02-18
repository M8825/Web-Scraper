import requests as req
from bs4 import BeautifulSoup
import string
import os


def get_title(soup):
    """Article title

    Removes punctuation marks and changes <space> with _ between words

    :param soup: response from server
    :return: Article Title
    """
    title = soup.find('h1', {'class': 'c-article-magazine-title'}).text
    title_punc = title.translate(title.maketrans('', '', string.punctuation))

    return title_punc.translate(title_punc.maketrans(' ', '_'))


def save_file(title, body, p):
    path = f'Page_{p}\{title}.txt'  # Saves into a folder associated with page_N

    file = open(path, 'w', encoding='UTF-8')
    file.write(body)
    file.close()


def pages_rec(articles, t, p, page=1):
    """
    Recursive function, requests data from server for every N page and parses
    the title and body from articles and saves in a page N associated folder

    :param articles: All articles from page
    :param t: Type of pages (News, Nature Briefing etc)
    :param p: Total amount of pages
    :param page: Current page number for recursion

    :return: Base case for recursion
    """
    if page > p:
        return

    for article in articles:
        articles_type = article.find(
            'span', {'data-test': 'article.type'}
        ).find('span')

        if articles_type.text.strip() == t:
            get_link = article.find(
                'a', {'data-track-action': 'view article'}
            )
            url = f"https://www.nature.com{get_link.get('href')}"
            r = req.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
            soup = BeautifulSoup(r.content, 'html.parser')

            title = get_title(soup)
            body = soup.find('div', {'class': 'c-article-body u-clearfix'}).text.strip()
            save_file(title, body, p)

    # Recursive for next page.
    url = f"https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year=2020&page={page}"
    r = req.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})

    soup = BeautifulSoup(r.content, 'html.parser')
    articles = soup.find_all('article')
    pages_rec(articles, t, p, page + 1)


def main():

    pages, tof_articles = int(input()), input()
    URL = "https://www.nature.com/nature/articles?sort=PubDate&year=2020"
    r = req.get(URL, headers={'Accept-Language': 'en-US,en;q=0.5'})

    if r.status_code != 200:
        print(f"The URL returned {r.status_code}!")
    else:
        soup = BeautifulSoup(r.content, 'html.parser')
        articles = soup.find_all('article')
        # Create folders based on the amount of pages.
        for i in range(pages):
            os.mkdir(f'Page_{i + 1}')

        pages_rec(articles, tof_articles, pages)


if __name__ == "__main__":
    main()
