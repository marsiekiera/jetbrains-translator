import requests
from bs4 import BeautifulSoup


def user_choice():
    language_dict = {
        1: "Arabic",
        2: "German",
        3: "English",
        4: "Spanish",
        5: "French",
        6: "Hebrew",
        7: "Japanese",
        8: "Dutch",
        9: "Polish",
        10: "Portuguese",
        11: "Romanian",
        12: "Russian",
        13: "Turkish"
    }
    print("Hello, you're welcome to the translator. Translator supports:")
    for lang in language_dict:
        print(str(lang) + ". " + language_dict[lang])
    while True:
        source_language_num = int(input("Type the number of your language:\n"))
        if source_language_num in range(1, len(language_dict) + 1):
            break
    while True:
        target_language_num = int(input("Type the number of language you want to translate to:\n"))
        if target_language_num in range(1, len(language_dict) + 1) and target_language_num != source_language_num:
            break
    word_to_translate = str(input('Type the word you want to translate: \n'))
    return {
        "source_language": language_dict[source_language_num].lower(),
        "target_language": language_dict[target_language_num].lower(),
        "word_to_translate": word_to_translate.lower()
    }


def site_request(user_choice_dict):
    lang_url = user_choice_dict["source_language"] + "-" + user_choice_dict["target_language"] + "/"
    url = "https://context.reverso.net/translation/" + lang_url + user_choice_dict["word_to_translate"]
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if r.status_code == 200:
        return url
    else:
        print("Connection error")
        exit()


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


def translation(url, target_language):
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(r.content, 'html.parser')
    words = soup.find_all("a", ["ltr", "dict"])
    sentences_list = []
    for div in soup.find_all("div", "ltr"):
        for span in div.find_all("span"):
            sentence = span.text.strip()
            if sentence:
                sentences_list.append(sentence)

    print(f"{target_language.capitalize()} Translations:")
    list_of_words(words)
    print(f"\n{target_language.capitalize()} Examples:")
    print_sentences(sentences_list)


def main():
    user_choice_dict = user_choice()
    url = site_request(user_choice_dict)
    translation(url, user_choice_dict["target_language"])


main()
