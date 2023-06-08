import random
import re


def get_random_color():
    return "#" + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])


def clean_text(text):
    return re.sub(r'-', ' ', re.sub(r'[",]', '', text)).lower()


def split_text_by_sentence(text):
    return re.split(r'(?<=[.!?])\s*', text)


def split_sentence_by_words(sentence):
    return re.findall(r'\b\S+\b', sentence)


def sort_data(data_):
    return {k: v for k, v in sorted(data_.items(), reverse=True, key=lambda item: item[1])}


def slice_dictionary(dict_: dict, start: int, finish: int):
    return {k: v for k, v in list(dict_.items())[start:finish]}


