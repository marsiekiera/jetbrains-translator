import requests

from bs4 import BeautifulSoup


def print_title(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    article = soup.find("h1")
    print(article.text)


print_title(input())
