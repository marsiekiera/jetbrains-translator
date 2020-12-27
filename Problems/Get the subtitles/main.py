import requests

from bs4 import BeautifulSoup


def print_subtitle(index, url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    articles = soup.find_all("h2")
    print(articles[index].text)


print_subtitle(int(input()), input())
