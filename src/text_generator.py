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
        extracted_text: str = ''
        html_doc: str = requests.get(url_).text
        soup = BeautifulSoup(html_doc, 'html.parser')
        for p in soup.find("h1", string="The Signal-Man").find_parent('div').find_all('p'):
            for br in p.find_all('br'):
                br.replace_with(" ")
            if "breadcrumb" in p.__str__():
                break
            extracted_text += p.text
        return extracted_text

    @classmethod
    def __calculate_transitions(cls, text: str):
        transitions: defaultdict = defaultdict(float)
        for sentence in split_text_by_sentence(text):
            words: list = split_sentence_by_words(sentence)
            for i in range(len(words) - 1):
                transitions[(words[i], words[i + 1])] += 1
        return transitions

    # coef = 0.5 if words[i] in ['the', 'a', 'is', 'are'] else 1
    # TODO solve the calculation way
    # for j in range(i + 1, len(›words) - 1):
    #     transitions[(words[i], words[j])] += 1 / (j - i)

    def generate_sentence(self) -> str:
        def get_next_word(curr_word: str):
            next_word_choices = [(transition[1], weight) for transition, weight in self.transitions_data.items() if
                                 transition[0] == curr_word]
            if len(next_word_choices) == 0:
                return False
            words, weights_ = zip(*next_word_choices)
            choice: str = random.choices(population=words, weights=weights_)[0]
            self.transitions_data[(curr_word, choice)] -= 1
            return choice

        sentence: list = []

        entry_word: str = random.choice(
            list(set([transition[0] for transition in self.transitions_data if
                      transition[0][0].isupper()])))

        while True:
            sentence.append(entry_word)
            if entry_word[len(entry_word) - 1] in '.!?':
                break
            entry_word = get_next_word(entry_word)
            if not entry_word:
                break

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
            file.write('Index,Word_1,Word_2,Frequency\n')
            ind: int = 1
            for k, v in self.transitions_data.items():
                file.write(f'{ind},{k[0]},{k[1]},{v}\n')
                ind += 1

    def get_bar_chart_image(self, bar_number: int) -> None:
        plt.figure(figsize=[15, 15])
        data_to_vis = slice_dictionary(self.transitions_data, 0, bar_number)
        objects = [f'{w1} {w2}' for w1, w2 in data_to_vis]
        values = data_to_vis.values()
        plt.bar(objects, values, color='green')
        plt.xticks(rotation=90)
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
