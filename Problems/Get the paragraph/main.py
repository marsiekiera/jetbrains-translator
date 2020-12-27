import requests

from bs4 import BeautifulSoup


def henry_stories(word, link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')
    paragraphs = soup.find_all('p')
    for paragraph in paragraphs:
        if word in paragraph.text:
            print(paragraph.text)
            break


henry_stories(input(), input())

