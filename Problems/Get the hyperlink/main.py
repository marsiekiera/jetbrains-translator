import requests

from bs4 import BeautifulSoup


def print_hyperlink(act, link):
    r = requests.get(link)
    if r.status_code != 200:
        return print("connection failed")
    soup = BeautifulSoup(r.content, 'html.parser')
    hrefs = soup.find_all('a')
    print(hrefs[act-1].get("href"))


print_hyperlink(int(input()), input())