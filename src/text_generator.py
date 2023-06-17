import random
from collections import defaultdict
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from pyvis.network import Network

from src.utils import clean_text, split_text_by_sentence, split_sentence_by_words, slice_dictionary, sort_data


class TextGenerator:
    def __init__(self, url_: str):
        self.source_url: str = url_
        self.text: str = clean_text(self.__get_text_from_url(self.source_url))
        self.transitions_data: dict = sort_data(self.__calculate_transitions(self.text))
        Path("../results/visualisation").mkdir(parents=True, exist_ok=True)
        Path("../results/data").mkdir(parents=True, exist_ok=True)

    @classmethod
    def __get_text_from_url(cls, url_: str) -> str:
        text = ''
        html_doc: str = requests.get(url_).text
        soup = BeautifulSoup(html_doc, 'html.parser')
        for p in soup.find("h1", string="The Signal-Man").find_parent('div').find_all('p'):
            for br in p.find_all('br'):
                br.replace_with(" ")
            if "breadcrumb" in p.__str__():
                break
            text += p.text
        return text

    @classmethod
    def __calculate_transitions(cls, text: str):
        transitions: defaultdict = defaultdict(float)
        for sentence in split_text_by_sentence(text):
            words: list = split_sentence_by_words(sentence)
            for i in range(len(words) - 1):
                # TODO solve the calculation way
                # for j in range(i + 1, len(words) - 1):
                #     transitions[(words[i], words[j])] += 1 / (j - i)
                coef = 0.5 if words[i] in ['the', 'a', 'is', 'are'] else 1
                transitions[(words[i], words[i + 1])] += coef
        return transitions

    def generate_sentence(self) -> str:
        def get_next_word(curr_word):
            next_word_choices = [(transition[1], weight) for transition, weight in self.transitions_data.items() if
                                 transition[0] == curr_word]
            if len(next_word_choices) == 0:
                return False
                # return random.choice(list(set([tup[0] for tup in self.transitions_data])))
            words, weights_ = zip(*next_word_choices)
            return random.choices(population=words, weights=weights_)[0]

        sentence: list = []

        entry_word = random.choice(
            list(set([transition[0] for transition in self.transitions_data if
                      transition[0][0].isupper()])))

        while True:
            sentence.append(entry_word)
            if entry_word[len(entry_word) - 1] in '.!?':
                break
            entry_word = get_next_word(entry_word)
            if not entry_word:
                break
            # if entry_word[0].isupper():
            #     entry_word= entry_word.lower()

        return " ".join(sentence)

    def generate_text(self, number_sentences) -> str:
        res = []
        for _ in range(number_sentences):
            res.append(self.generate_sentence())
        res = " ".join(res)
        with open("../results/data/generated_text.txt", 'w') as file:
            file.write(res)
        return res

    def write_data_to_file(self) -> None:
        with open('../results/data/transitions.csv', 'w') as file:
            file.write('Word 1, Word 2, Frequency\n')
            for k, v in self.transitions_data.items():
                file.write(f'{k[0]}, {k[1]}, {v}\n')

    def get_bar_chart_image(self, bar_number: int) -> None:
        if bar_number > 20:
            raise Exception('More than 20 will look ugly')
        data_to_vis = slice_dictionary(self.transitions_data, 0, bar_number)
        objects = [f'{w1} {w2}' for w1, w2 in data_to_vis]
        values = data_to_vis.values()
        plt.bar(objects, values, color='green')
        plt.xticks(rotation=45)
        plt.xlabel('Transitions')
        plt.ylabel('Frequency')
        plt.title(f'Top {len(data_to_vis)} transitions')
        plt.tight_layout()
        plt.savefig('../results/visualisation/top_transitions.png')
        plt.show()

    def get_graph_html(self, nodes_number: int) -> None:
        graph = Network(height="750px", width='100%', bgcolor="#FFFFFF", directed=True,
                        )
        graph.barnes_hut()
        data_to_vis = slice_dictionary(self.transitions_data, 0, nodes_number)
        for key in data_to_vis:
            graph.add_node(n_id=key[0], label=key[0], title=key[0], color="#6da33e")
            graph.add_node(n_id=key[1], label=key[1], title=key[1], color="#6da33e")
            graph.add_edge(key[0], key[1], value=data_to_vis[key])
        graph.save_graph("../results/visualisation/graph.html")
