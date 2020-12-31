import requests
from bs4 import BeautifulSoup
import sys

# Dictionary of all language
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


def user_choice():
    """Get the value from the user.
    Return dictionary with 4 item:
    source_language (str), target_language(str),
    word_to_translate (str), all_language (bool)"""
    args = sys.argv
    source_languages_list = []
    for language in language_dict:
        source_languages_list.append(language_dict[language].lower())
    target_languages_list = source_languages_list
    target_languages_list.append("all")
    if len(args) != 4:
        print("""The script should be called with three arguments, first - source language, 
        second - target language, third - word to translate""")
        exit()
    source_language = args[1].lower()
    target_language = args[2].lower()
    word_to_translate = args[3].lower()
    all_languages = False
    if ((source_language not in source_languages_list) or
            (target_language not in target_languages_list)):
        exit()
    if target_language == "all":
        all_languages = True
    return {
        "source_language": source_language,
        "target_language": target_language,
        "word_to_translate": word_to_translate,
        "all_languages": all_languages
    }


# def user_choice():
#     """Get the value from the user.
#     Return dictionary with 4 item:
#     source_language (str), target_language(str),
#     word_to_translate (str), all_language (bool)"""
#     all_languages = False
#     print("Hello, you're welcome to the translator. Translator supports:")
#     for lang in language_dict:
#         print(str(lang) + ". " + language_dict[lang])
#     while True:
#         source_language_num = int(input("Type the number of your language:\n"))
#         if source_language_num in range(1, len(language_dict) + 1):
#             break
#     while True:
#         target_language_num = int(input(
#             "Type the number of language you want to translate to or '0' to translate to all languages:\n"))
#         if target_language_num in range(0, len(language_dict) + 1) and target_language_num != source_language_num:
#             break
#     word_to_translate = str(input('Type the word you want to translate: \n'))
#     if target_language_num == 0:
#         all_languages = True
#         target_language = "all"
#     else:
#         target_language = language_dict[target_language_num].lower()
#     return {
#         "source_language": language_dict[source_language_num].lower(),
#         "target_language": target_language,
#         "word_to_translate": word_to_translate.lower(),
#         "all_languages": all_languages
#     }


def create_url(user_choice_dict):
    """Create url containing source and target languages and word, from dictionary
    Return url (str) end target_language (str) if website allows for translation,
    otherwise return False (bool)"""
    if (user_choice_dict["source_language"] == "russian"
            and user_choice_dict["target_language"] in ["polish", "romanian", "turkish"]):
        return False
    else:
        lang_url = user_choice_dict["source_language"] + "-" + user_choice_dict["target_language"] + "/"
        url = "https://context.reverso.net/translation/" + lang_url + user_choice_dict["word_to_translate"]
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if r.status_code == 200:
            return url, user_choice_dict["target_language"]
        else:
            print("Connection error")
            exit()


def create_url_list(user_choice_dict):
    """Return url_list (list) containing all languages as target_language"""
    url_list = []
    for lang in language_dict:
        user_choice_dict["target_language"] = language_dict[lang].lower()
        if user_choice_dict["source_language"] != language_dict[lang].lower():
            url = create_url(user_choice_dict)
            if url:
                url_list.append(url)
    return url_list


def translation(url, target_language):
    """Create translation lists.
    Get url (str) and target_language (str).
    Return list with words_list (list), sentence_list (list) and target_language (str)."""
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(r.content, 'html.parser')
    words = soup.find_all("a", ["ltr", "dict"])
    sentences_list = []
    for div in soup.find_all("div", "ltr"):
        for span in div.find_all("span"):
            sentence = span.text.strip()
            if sentence:
                sentences_list.append(sentence)
    sentences_list = sentences_list[0:10]
    words_list = []
    for word in words:
        words_list.append(word.text.strip())
    words_list = words_list[:5]
    return [words_list, sentences_list, target_language]


def create_file_one_language(translation_list, word):
    """Get list with words_list (list), sentence_list (list) and target_language (str).
    Create text file word.txt"""
    text_file = open(f"{word}.txt", "w", encoding="UTF-8")
    words_list, sentences_list, target_language = translation_list
    text_file.write(f"{target_language.capitalize()} Translations:\n")
    for word in words_list:
        text_file.write(f"{word}\n")
    text_file.write("\n\n")
    text_file.write(f"{target_language.capitalize()} Example:\n")
    counter = 0
    for sentence in sentences_list:
        if counter < 2:
            text_file.write(f"{sentence}\n")
            counter += 1
        elif counter > 1:
            text_file.write(f"\n{sentence}\n")
            counter = 1
    text_file.close()


def create_file_all_languages(url_list, word):
    """Create text file word.txt"""
    text_file = open(f"{word}.txt", "w", encoding="UTF-8")
    for url in url_list:
        words_list, sentences_list, target_language = translation(url[0], url[1])
        text_file.write(f"{target_language.capitalize()} Translations:\n")
        text_file.write(f"{words_list[0]}\n\n")
        text_file.write(f"{target_language.capitalize()} Example:\n")
        text_file.write(f"{sentences_list[0]}\n")
        text_file.write(f"{sentences_list[1]}")
        if url != url_list[-1]:
            text_file.write("\n\n\n")
    text_file.close()


def read_text_file(word):
    """Read text file word.txt and print them out"""
    text_file = open(f"{word}.txt", "r", encoding="UTF-8")
    print(text_file.read())
    text_file.close()


def main():
    """Translates the word given by the user in a given language
    into another selected language or all available languages."""
    user_choice_dict = user_choice()
    word_to_translate = user_choice_dict["word_to_translate"].lower()
    target_language = user_choice_dict["target_language"].lower()
    if user_choice_dict["all_languages"]:
        url_list = create_url_list(user_choice_dict)
        create_file_all_languages(url_list, word_to_translate)
        read_text_file(word_to_translate)
    else:
        url_bool = create_url(user_choice_dict)
        # Check if website allows to translate between languages
        if url_bool:
            url = url_bool[0]
            create_file_one_language(
                translation(url, target_language), word_to_translate)
            read_text_file(word_to_translate)
        else:
            exit()


main()
