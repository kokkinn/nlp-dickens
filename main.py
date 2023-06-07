import random

import requests
import re
from bs4 import BeautifulSoup
from collections import defaultdict


def get_text_from_url() -> str:
    text = ''
    url: str = "https://www.online-literature.com/dickens/2941/"
    response: requests.Response = requests.get(url)
    html_doc: str = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    anchor = soup.find("h1", string="The Signal-Man")
    text_object = anchor.find_parent('div')
    paragraphs = text_object.find_all('p')
    for p in paragraphs:
        for br in p.find_all('br'):
            br.replace_with(" ")
        if "breadcrumb" in p.__str__():
            break
        text += p.text
    return text


# TODO place regex in constants
def clean_text(text):
    return re.sub(r'[\n"]', '', text).lower()


def split_text_by_sentence(text):
    return re.split(r'(?<=[.!?])\s*', text)


def split_sentence_by_words(sentence):
    return re.findall(r'\b\S+\b', sentence)


def calculate_transitions(text):
    transitions: defaultdict = defaultdict(float)
    for sentence in split_text_by_sentence(text):
        words: list = split_sentence_by_words(sentence)
        for i in range(len(words) - 1):
            # for j in range(i + 1, len(words) - 1):
            #     transitions[(words[i], words[j])] += 1 / (j - i)
            coef = 0.5 if words[i] in ['the', 'a', 'is', 'are'] else 1
            transitions[(words[i], words[i + 1])] += coef
    return transitions


def write_data_to_file(data_):
    file_res = open('result', 'w')
    for k, v in data_.items():
        file_res.write(f'{k}: {v}\n')


def sort_data(data_):
    return {k: v for k, v in sorted(data_.items(), reverse=True, key=lambda item: item[1])}


def generate_sentence(transitions_data: dict, words_number: int, entry_word: str = None):
    def get_next_word(curr_word):
        next_word_choices = [(transition[1], weight) for transition, weight in transitions_data.items() if
                             transition[0] == curr_word]
        if len(next_word_choices) == 0:
            return random.choice(list(set([tup[0] for tup in transitions_data])))
        words, weights_ = zip(*next_word_choices)
        return random.choices(population=words, weights=weights_)[0]

    sentence: list = []

    if entry_word is None:
        entry_word = random.choice(list(set([tup[0] for tup in transitions_data])))

    for _ in range(words_number):
        sentence.append(entry_word)
        entry_word = get_next_word(entry_word)

    sentence[0] = sentence[0].capitalize()
    return " ".join(sentence) + (random.choice(['.']))


def generate_text(number_sentences: int, data_) -> str:
    res = []
    for _ in range(number_sentences):
        res.append(generate_sentence(data_, random.randint(4, 20), random.choice(['I', "my", 'A', 'The'])))
    return " ".join(res)

# print(get_text_from_url())
data = calculate_transitions(get_text_from_url())
# write_data_to_file(sort_data(data))
print(generate_text(5, data))
