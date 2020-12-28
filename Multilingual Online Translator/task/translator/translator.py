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
        print("200 OK\n")
    else:
        return exit()
    return url


def list_of_words(words):
    words_list = []
    for word in words:
        words_list.append(word.text.strip())
    words_list = words_list[:5]
    for word in words_list:
        print(word)


def print_sentences(sentences_list):
    counter = 0
    for sentence in sentences_list[0:10]:
        if counter < 2:
            print(sentence)
            counter += 1
        elif counter > 1:
            print()
            print(sentence)
            counter = 1


def translation(url, lang_choice):
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(r.content, 'html.parser')
    words = soup.find_all("a", ["ltr", "dict"])
    sentences_list = []
    for div in soup.find_all("div", "ltr"):
        for span in div.find_all("span"):
            sentence = span.text.strip()
            if sentence:
                sentences_list.append(sentence)
    print("Context examples:\n")
    if lang_choice == "fr":
        print("French Translations:")
    else:
        print("English Translations:")
    list_of_words(words)
    print()
    if lang_choice == "fr":
        print("French Examples:")
    else:
        print("English Examples:")
    print_sentences(sentences_list)


def main():
    lang_choice, word_to_trans = user_choice()
    translation(site_request(lang_choice, word_to_trans), lang_choice)


main()
