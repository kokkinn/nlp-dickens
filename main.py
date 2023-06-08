import random
import requests
import re
from bs4 import BeautifulSoup
from collections import defaultdict
from pyvis.network import Network
import matplotlib.pyplot as plt


def get_random_color():
    return "#" + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])


def clean_text(text):
    return re.sub(r'[\n"]', '', text).lower()


def split_text_by_sentence(text):
    return re.split(r'(?<=[.!?])\s*', text)


def split_sentence_by_words(sentence):
    return re.findall(r'\b\S+\b', sentence)


def sort_data(data_):
    return {k: v for k, v in sorted(data_.items(), reverse=True, key=lambda item: item[1])}


def slice_dictionary(dict_: dict, start: int, finish: int):
    return {k: v for k, v in list(dict_.items())[start:finish]}


class TextGenerator:
    def __init__(self, url_: str):
        self.source_url: str = url_
        self.text: str = self.__get_text_from_url(self.source_url)
        self.transitions_data: dict = sort_data(self.__calculate_transitions(self.text))

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
                # for j in range(i + 1, len(words) - 1):
                #     transitions[(words[i], words[j])] += 1 / (j - i)
                coef = 0.5 if words[i] in ['the', 'a', 'is', 'are'] else 1
                transitions[(words[i], words[i + 1])] += coef
        return transitions

    def generate_sentence(self, words_number: int, entry_word: str = None):
        def get_next_word(curr_word):
            next_word_choices = [(transition[1], weight) for transition, weight in self.transitions_data.items() if
                                 transition[0] == curr_word]
            if len(next_word_choices) == 0:
                return random.choice(list(set([tup[0] for tup in self.transitions_data])))
            words, weights_ = zip(*next_word_choices)
            return random.choices(population=words, weights=weights_)[0]

        sentence: list = []

        if entry_word is None:
            entry_word = random.choice(list(set([tup[0] for tup in self.transitions_data])))

        for _ in range(words_number):
            sentence.append(entry_word)
            entry_word = get_next_word(entry_word)

        sentence[0] = sentence[0].capitalize()
        return " ".join(sentence) + (random.choice(['.']))

    def generate_text(self, number_sentences) -> str:
        res = []
        for _ in range(number_sentences):
            res.append(self.generate_sentence(random.randint(4, 20), random.choice(['I', "my", 'A', 'The'])))
        return " ".join(res)

    def write_data_to_file(self):
        with open('results/data/transitions.csv', 'w') as file:
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
        plt.savefig('results/visualisation/top_transitions.png')
        plt.show()

    def get_graph_html(self, nodes_number: int) -> None:
        graph = Network(height="750px", width='750px', bgcolor="", font_color="#000", directed=True,
                        )
        graph.barnes_hut()
        data_to_vis = slice_dictionary(self.transitions_data, 0, nodes_number)
        for key in data_to_vis:
            graph.add_node(n_id=key[0], label=key[0], title=key[0], color="#6da33e")
            graph.add_node(n_id=key[1], label=key[1], title=key[1], color="#6da33e")
            graph.add_edge(key[0], key[1], value=data_to_vis[key])
        graph.save_graph("results/visualisation/graph.html")


def main():
    url: str = "https://www.online-literature.com/dickens/2941/"
    tg1 = TextGenerator(url)
    # tg1.get_graph_html(100)
    tg1.write_data_to_file()


if __name__ == '__main__':
    main()
