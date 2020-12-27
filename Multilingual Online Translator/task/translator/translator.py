import requests

from bs4 import BeautifulSoup


def user_choice():
    lang_choice = ""
    while lang_choice not in ['en', 'fr']:
        lang_choice = str(input(
            '''Type "en" if you want to translate from French into English, 
            or "fr" if you want to translate from English into French:\n '''))
    word_to_trans = str(input('Type the word you want to translate: \n'))
    print(f'You chose "{lang_choice}" as the language to translate "{word_to_trans}" to.')
    return [lang_choice, word_to_trans]


def site_request(lang, word):
    lang_url = "english-french/" if lang == "fr" else "french-english/"
    url = "https://context.reverso.net/translation/" + lang_url + word
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if r.status_code == 200:
        print("200 OK")
    else:
        return exit()
    return url


def translation(url):
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(r.content, 'html.parser')
    words = soup.find_all("a", ["ltr", "dict"])
    words_list = []
    for word in words:
        words_list.append(word.text.strip())
    sentences_list = []
    for div in soup.find_all("div", "ltr"):
        for span in div.find_all("span"):
            sentence = span.text.strip()
            if sentence:
                sentences_list.append(sentence)
    print("Translations")
    print(words_list)
    print(sentences_list)


def main():
    user_choices = user_choice()
    translation(site_request(user_choices[0], user_choices[1]))


main()
